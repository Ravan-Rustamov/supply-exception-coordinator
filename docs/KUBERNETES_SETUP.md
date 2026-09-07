# Kubernetes Cluster Setup — Day 2 Complete

## Topology

## Setup Steps Completed

### 1. SSH & Network ✅
- SSH keys generated (parolasız bağlantı)
- `/etc/hosts` configured (tüm 3 maşında)
- Hostname-lər değiştirildi

### 2. Kernel & Docker ✅
- overlay, br_netfilter modulları
- sysctl: ip_forward, bridge-nf-call
- Docker v29.1.3 (tüm maşında)
- kubeadm v1.31.14

### 3. Kubernetes Control Plane ✅
```bash
kubeadm init --pod-network-cidr=10.244.0.0/16
```
- Master: READY
- Flannel CNI: deployed
- API server: healthy

### 4. Workers Joined ✅
```bash
kubeadm join 10.10.100.50:6443 --token <token> ...
```
- worker1: READY
- worker2: joining (Day 3)

## Check Status
```bash
kubectl get nodes -o wide
kubectl get pods -A
```

## Next Steps
- [ ] Worker-2 kubeadm join (new token needed if >24h)
- [ ] All nodes READY
- [ ] Deploy supply-exception-coordinator
