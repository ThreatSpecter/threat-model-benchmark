# kata-containers

Kata Containers — Hardware Virtualisation Isolation Layer — Kata Containers provides a second layer of isolation on top of traditional container isolation by running each pod inside a lightweight virtual machine. This scope covers the attack surface of the hardware virtualisation interface — specifically the virtio device backends, VMM processes, and ACPI subsystem — that separates the untrusted container workload inside the VM from the host infrastructure. The threat model evaluates whether a malicious container workload or its user can escape the VM boundary, tamper with the host, obtain information from the host or other VMs, or cause denial of service through the defined attack surfaces. Kata Containers prevents an untrusted container workload or user of that container workload from gaining control of, obtaining information from, or tampering with host infrastructure. This threat model analyses the attack surface of each virtio device interface (virtio-blk, virtio-scsi, virtio-fs, virtio-net, virtio-vsock), device passthrough (VFIO), and dynamic resource management (ACPI/hotplug) across four supported VMMs: QEMU, Firecracker, Cloud Hypervisor and Dragonball. Source: kata-containers/kata-containers, Apache 2.0 license (https://github.com/kata-containers/kata-containers/blob/main/docs/threat-model/threat-model.md). Boundary diagram: https://github.com/kata-containers/kata-containers/blob/main/docs/threat-model/threat-model-boundaries.svg. Tags: container-isolation, virtualisation, kata-containers, cncf, virtio, kubernetes, confidential-computing. Contributors: [your name here]. Note: Repudiation is explicitly out of scope — the source document does not address logging, auditing, or non-repudiation mechanisms.

## Components
- Container Workload
- Kata Agent
- CRI Runtime (containerd / cri-o)
- Virtual Machine Monitor / Hypervisor (KVM + VMM)
- virtio-blk / virtio-scsi Storage Backend
- virtiofsd (vhost-user Filesystem Daemon)
- virtio-net Backend
- virtio-vsock Backend (Control Channel)
- VFIO Device Passthrough
- ACPI / Hotplug Subsystem
- Host Filesystem (virtio-fs Shared Directory)
- Host Physical Memory

## Data flows
- container-workload → virtio-blk-scsi
- container-workload → virtiofsd
- container-workload → virtio-net-backend
- kata-agent → virtio-vsock-backend
- vfio-device-passthrough → host-physical-memory
- cri-runtime → vmm-hypervisor
- vmm-hypervisor → acpi-hotplug
- container-user → container-workload
- virtiofsd → host-filesystem

## Trust zones
- Container Workload (b0)
- Guest Userspace (b1)
- Host Userspace (b3)
- Host Kernel