# Copyright 2023 Bluequbit Inc.
#
# All Rights Reserved
#
# NOTICE: All information contained herein is, and remains the property of Bluequbit Inc.
# and its suppliers, if any. The intellectual and technical concepts contained herein are
# proprietary to Bluequbit Inc. and its suppliers and may be covered by U.S. and Foreign Patents,
# patents in process, and are protected by trade secret or copyright law.
# Dissemination of this information or reproduction of this material is strictly forbidden unless
# prior written permission is obtained from Bluequbit Inc.
#
# This file is part of a proprietary software product and is not to be copied, modified,
# redistributed, or used in any way without the express written permission of Bluequbit Inc.


import pennylane as qml
from pennylane import numpy as np
from scipy.sparse import diags
from tqdm.notebook import trange

complex_dtype = np.complex128
real_dtype = np.float64


class AdamOptim:
    def __init__(self, eta=0.03, beta1=0.9, beta2=0.999, epsilon=1e-8):
        super().__init__()
        self.m, self.v = 0, 0
        self.beta1 = beta1
        self.beta2 = beta2
        self.epsilon = epsilon
        self.eta = eta
        self.t = 1

    def step(self, grad):
        ## dw, db are from current minibatch
        ## momentum beta 1
        self.m = self.beta1 * self.m + (1 - self.beta1) * grad
        ## rms beta 2
        self.v = self.beta2 * self.v + (1 - self.beta2) * (grad**2)
        ## bias correction
        m_corr = self.m / (1 - self.beta1**self.t)
        v_corr = self.v / (1 - self.beta2**self.t)
        self.t += 1
        ## update weights and biases
        return self.eta * (m_corr / (np.sqrt(v_corr) + self.epsilon))


def _get_circuit_info(circuit):
    # todo: assert circuit is qnode
    params_dummy = np.zeros(1000000, requires_grad=True)
    specs = qml.specs(circuit)(params_dummy)
    num_params = specs[
        "num_trainable_params"
    ]  # one way to get number of params from a circuit
    num_wires = specs["resources"].num_wires
    return num_wires, num_params


def load_data(
    target_probs: np.ndarray,
    circuit_fn,  #: a QNode-able function (if it's QNode, it will work but very slow)
    num_wires: int,
    seed: int = 0,
    loss_type: str = "kl-divergence",
    num_epochs: int = 1000,
    params_init=None,
    eta=0.03,
):
    r"""Run QCBM training to find an approximation to the target_distribution"""
    if loss_type != "kl-divergence":
        print(
            f"WARNING: Got unsupported loss_type {loss_type}: falling back to kl-divergence"
        )
        loss_type = "kl-divergence"
    dev_gpu = qml.device("lightning.gpu", wires=num_wires, c_dtype=complex_dtype)
    circuit = qml.QNode(circuit_fn, dev_gpu)
    num_wires, num_params = _get_circuit_info(circuit)
    circuit_adj = qml.QNode(
        circuit_fn, dev_gpu, diff_method="adjoint", device_vjp=False
    )

    def adjoint_kl_native(params):
        wires = range(num_wires)
        ket = circuit(params).astype(complex_dtype)
        obs = -target_probs / (ket * ket.conj())
        hmat = diags(obs, format="csr")
        h = qml.SparseHamiltonian(hmat, wires)
        grad = qml.grad(circuit_adj)(params, h)
        loss = np.sum(target_probs * np.log(target_probs / (np.abs(ket) ** 2)))
        return grad, loss, ket

    np.random.seed(seed)
    best_x, best_loss = None, np.inf
    if params_init is None:
        x = np.random.rand(num_params, requires_grad=True).astype(real_dtype)
    else:
        x = np.zeros(num_params, requires_grad=True).astype(real_dtype)
        x[: len(params_init)] = params_init
    print(f"starting training with qubits: {num_wires} params: {num_params}")
    print(qml.specs(circuit)(x)["resources"])
    #     print(qml.draw(circuit_gpu)(x))
    opt = AdamOptim(eta=eta)
    break_points: dict[int, float] = {}
    # break_points = {100: 1.22, 200: 1.04, 300: 0.98, 400: 0.95, 600: 0.9,
    #                 900: 0.8, 1200 : 0.75, 1500: 0.7}
    loss = np.inf
    for epoch in trange(num_epochs):
        if epoch in break_points and loss > break_points[epoch]:
            print(f"CUTTING SHORT...{loss} > {break_points[epoch]} ")
            break
        grad, loss, pred_state = adjoint_kl_native(x)
        grad = np.array(grad).astype(real_dtype)
        if loss < best_loss:
            best_loss = loss
            if best_loss < 8 and epoch % 1 == 0:
                pred_state = circuit(x)
                l1_loss = np.sum(np.abs(target_probs - np.abs(pred_state) ** 2))
                print(
                    f"NEW* best_loss: {best_loss}: qubits: {num_wires} L1_loss: {l1_loss}"
                )
            best_x = x.copy()
        x -= opt.step(grad)
        print(f"epoch: {epoch} \t loss: {loss} \t", flush=True)
    return best_x, best_loss
