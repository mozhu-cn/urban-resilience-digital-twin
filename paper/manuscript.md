# A Physics-Guided Digital Twin Framework for Urban Infrastructure Resilience Assessment under Extreme Flooding: Integrating Terrain-Informed Flood Simulation, Delayed Cascading Failures, and Adaptive Restoration

**Authors:** Zheyu Huang\*, Yujia Huang
(\*Corresponding author: zheyu.huang@example.edu)

---

## Abstract

Extreme flooding poses increasing risks to urban systems due to the combined impacts of climate change, rapid urbanization, and growing interdependencies among critical infrastructures. Existing urban resilience assessment approaches predominantly rely on static vulnerability indicators or isolated infrastructure analysis, which are insufficient to capture the dynamic evolution of flood hazards, cascading failures, and adaptive recovery processes. To address this limitation, this study proposes a physics-guided digital twin framework for dynamic urban flood resilience assessment and adaptive recovery optimization.

The proposed framework integrates four coupled components: (1) a terrain-informed cellular flood simulation model for high-resolution hazard evolution, (2) a multi-layer infrastructure network model for representing interdependent system behavior, (3) a time-delayed cascading failure analysis for capturing failure propagation among power and communication infrastructures, and (4) an adaptive restoration optimization module for supporting dynamic emergency response decisions under flood-constrained transportation. A spatiotemporal digital twin environment is developed to continuously update urban system states by coupling physical hazard processes, infrastructure conditions, and recovery strategies.

A case study of Miyazaki City, Japan, is conducted to evaluate the proposed framework under an extreme typhoon rainfall scenario with a peak intensity of 100 mm/h. The results demonstrate that the framework can effectively reproduce nonlinear flood propagation driven by heterogeneous terrain and drainage saturation, identify spatial distributions of infrastructure exposure, and reveal delayed cascading failure mechanisms caused by infrastructure interdependencies and backup-energy depletion. Compared with conventional fixed-priority restoration strategies and non-intervention scenarios, the proposed adaptive restoration approach improves recovery efficiency by dynamically allocating limited repair resources according to system conditions and infrastructure criticality. Sensitivity analyses further highlight the significant effects of rainfall intensity, drainage capacity, backup-battery duration, and repair-resource availability on urban resilience performance.

This study contributes a comprehensive and computationally reproducible digital twin framework that bridges physical flood modeling, infrastructure resilience analysis, and intelligent recovery decision-making. The proposed approach provides a practical foundation for next-generation urban resilience planning, emergency management, and climate adaptation under increasing flood risks.

**Keywords:** Urban resilience; Digital twin; Cellular automata flood simulation; Interdependent infrastructure networks; Cascading failures; Adaptive restoration; Critical infrastructure protection

---

## 1. Introduction

Climate change has intensified the frequency and severity of extreme precipitation events, making urban flooding one of the most significant threats to sustainable urban development [1]. Unlike conventional natural hazards that affect isolated components, extreme floods increasingly interact with interconnected urban infrastructure systems, including power supply networks, communication networks, transportation systems, and water management facilities [2]. The increasing dependence among these systems introduces complex failure propagation mechanisms, where localized physical damage can trigger large-scale cascading disruptions across multiple infrastructure domains [3, 4].

Critical infrastructure systems (CIS) are characterized by strong physical and functional interdependencies. For example, communication networks rely on continuous power supply, while emergency response activities require functioning transportation systems [5]. Consequently, failures occurring in one infrastructure layer may propagate into other layers through dependency relationships, potentially leading to nonlinear system degradation and prolonged recovery periods [6]. Therefore, accurately evaluating infrastructure resilience requires not only identifying vulnerable components but also reproducing the dynamic interactions among hazards, infrastructure failures, and recovery interventions [7, 8].

Existing studies have investigated infrastructure vulnerability and cascading failures from various perspectives. Complex network theory and percolation-based approaches have provided valuable insights into the structural robustness of interdependent networks [9, 10, 4]. However, many existing models simplify disaster impacts as instantaneous node failures or probabilistic disturbances, without explicitly considering the underlying physical processes that generate infrastructure damage [11].

One major limitation concerns the representation of flood hazards. Many urban flood resilience studies adopt simplified approaches such as bathtub models, uniform water-level assumptions, or distance-based hazard indicators. Although computationally efficient, these approaches neglect the influence of heterogeneous urban topography, surface runoff pathways, and nonlinear drainage limitations [12]. In reality, flood propagation is governed by complex interactions among rainfall intensity, terrain gradients, drainage capacity, and local accumulation processes [13, 14].

Another limitation lies in the temporal characteristics of infrastructure failure. Conventional cascading failure models frequently assume immediate failure propagation after dependency loss [3]. However, practical infrastructure systems often contain redundancy mechanisms that provide temporary operational capability — for instance, communication facilities are commonly equipped with backup batteries or uninterrupted power supply systems [15]. This delayed failure mechanism introduces an important resilience buffer, creating a temporal window for emergency intervention.

Furthermore, many current digital twin and resilience assessment frameworks primarily focus on damage simulation while neglecting the active role of emergency restoration [16, 17, 18]. In real disaster scenarios, recovery operations occur within rapidly changing physical environments; floodwaters may dynamically block transportation networks, alter travel accessibility, and increase response delays [19].

To address these limitations, this study develops a high-resolution four-dimensional digital twin framework that integrates physical flood dynamics, infrastructure interdependency, and adaptive restoration processes within a unified simulation environment. The main contributions of this study are:

1. **High-resolution flood dynamics modeling.** A terrain-informed cellular automata (CA) flood propagation model is developed using high-resolution elevation data, incorporating heterogeneous drainage capacity and subsurface storage limitations to reproduce nonlinear urban flood evolution and identify critical flooding transition points.
2. **Time-delayed cascading failure mechanism.** A coupled power–communication infrastructure model integrates flood-induced physical damage with backup-battery depletion dynamics, capturing delayed failure propagation and revealing the temporal characteristics of cascading disruptions.
3. **Dynamic restoration optimization under flood constraints.** A human-in-the-loop restoration mechanism couples flood-dependent road accessibility, dynamic shortest-path routing, and multi-objective emergency prioritization.

The remainder of this paper is organized as follows. Section 2 reviews related studies. Section 3 presents the proposed digital twin framework and mathematical formulations. Section 4 introduces the case study and experimental design. Section 5 discusses simulation results and comparative analyses. Section 6 provides further discussion of practical implications and limitations. Section 7 concludes the study.

## 2. Related Work

### 2.1 Digital Twins in Urban Disaster Management

Digital twin technology has emerged as an effective approach for representing complex urban systems by integrating physical entities, sensing data, computational models, and decision-support mechanisms [17, 18]. Urban digital twins have been increasingly applied in infrastructure monitoring, smart city management, and disaster response [16]. However, many current applications focus on data integration, visualization, and asset management, while the dynamic coupling between hazard evolution and infrastructure response remains insufficiently explored. For flood resilience assessment, an effective digital twin should not only reproduce the spatial distribution of hazards but also capture the temporal interactions between environmental processes, infrastructure degradation, and recovery actions.

### 2.2 Flood Simulation and Urban Flood Dynamics Modeling

Traditional hydrodynamic models based on shallow-water equations (SWE) provide physically meaningful flood propagation simulations [12]; however, they often require detailed hydraulic parameters and considerable computational resources, limiting their application in large-scale real-time digital twin environments. Cellular automata-based flood models have attracted increasing attention due to their computational efficiency and capability of representing spatially distributed flood evolution [14, 13, 20]. However, existing CA-based approaches are often developed independently from infrastructure systems and mainly focus on flood extent prediction rather than disaster-induced functional degradation.

### 2.3 Cascading Failure Modeling in Interdependent Infrastructure Networks

Modern cities rely on highly interconnected infrastructure networks [2]. Previous studies have developed various network-based approaches to analyze cascading failures, including graph theory models, percolation theory, agent-based simulations, and reliability-based approaches [5]. These methods have significantly improved the understanding of infrastructure vulnerability under disruptive events. However, several limitations remain: (i) failures are often assumed instantaneous, neglecting temporal delays associated with degradation and backup operation [11]; (ii) networks are frequently analyzed independently while real urban systems exhibit complex cross-network dependencies [6]; and (iii) most models provide limited integration with recovery decision-making processes.

### 2.4 Resilience Assessment and Adaptive Recovery Optimization

Urban resilience has evolved from a concept focusing on resistance and robustness toward a broader perspective incorporating absorption, adaptation, and recovery capabilities [21, 7]. Existing assessment methods commonly use performance-based indicators, resilience curves, and recovery trajectories [8, 6]. Although these approaches provide valuable evaluation frameworks, recovery planning is often treated as an independent optimization problem after disaster occurrence [11]. Integrating adaptive restoration optimization into a dynamic digital twin environment remains an open research direction.

### 2.5 Research Gaps and Motivation

Three major research gaps are identified: (1) urban digital twins emphasize data integration and visualization over coupled hazard–infrastructure dynamics; (2) flood simulation and infrastructure resilience models are often developed separately; and (3) recovery optimization relies on static strategies without adapting to changing disaster conditions. This study addresses these gaps with a unified physics-guided spatiotemporal digital twin framework.

## 3. Methodology

### 3.1 Overview of the Proposed Digital Twin Framework

The proposed framework integrates three coupled components: (1) a terrain-driven flood evolution model based on cellular automata, (2) an interdependent infrastructure failure model incorporating time-delayed cascading effects, and (3) a dynamic restoration optimization module considering flood-induced transportation constraints. At each simulation cycle, rainfall forcing is introduced into the physical environment; the CA-based flood model updates the spatial flood distribution; the flood field determines the physical status of infrastructure components; cascading failure dynamics are calculated through dependency relationships; and emergency restoration decisions are generated according to current network conditions. The complete interaction process is:

**Rainfall → Flood evolution → Infrastructure damage → Cascading failure → Dynamic restoration → Resilience update** (Eq. 1)

### 3.2 Terrain Reconstruction and Physical Environment Model

The study area is discretized into a two-dimensional regular cellular grid **C** = {C(i,j) | i = 1,…,Nx, j = 1,…,Ny} (Eq. 2), with Nx = Ny = 650 in the case study (422,500 spatial cells). Terrain elevation is reconstructed by spatial interpolation and Gaussian smoothing Z(i,j) = (Gσ * Z0)(i,j) (Eq. 3, σ = 0.8). The local slope magnitude S(i,j) (Eq. 4) is normalized to Ŝ(i,j) ∈ [0,1], which drives the spatial heterogeneity of drainage capacity and subsurface storage.

### 3.3 Terrain-Informed Cellular Flood Propagation Model

The CA model follows three principles: local mass conservation between neighboring cells; gravity-driven water redistribution according to hydraulic head differences; and adaptive drainage response constrained by local environmental characteristics.

**Rainfall and hydraulic head.** Rainfall is converted into water depth increments: W\*(i,j,t) = W(i,j,t) + R(t) (Eq. 5); the hydraulic head is H(i,j,t) = Z(i,j) + W\*(i,j,t) (Eq. 6).

**Flux exchange.** For each direction d ∈ {N,S,E,W}, the positive head difference ΔHd⁺ = max(0, H − Hd) is computed, and the maximum transferable water volume is Qlim = α·W\* (Eq. 7). Directional fluxes are allocated proportionally: Qd = (ΔHd⁺/ΔHtotal)·Qlim (Eq. 8). The CFL condition requires 4α ≤ 1; we set α = 0.12.

**Drainage and storage saturation.** The effective drainage rate is D(i,j) = D0(1 + η·Ŝ(i,j)) (Eq. 9). The actual drainage volume is constrained by water availability, drainage rate, and remaining subsurface storage K(i,j,t): Dact = min(W\*, D·Δt, K) (Eq. 10), with K(i,j,t+Δt) = max(0, K − Dact) (Eq. 11). When K = 0, the drainage system reaches saturation and additional rainfall contributes directly to surface flooding — a nonlinear tipping point.

**Water depth update.** W(i,j,t+Δt) = W(i,j,t) − ΣQd^out + ΣQd^in − Dact (Eq. 12), ensuring local mass conservation.

### 3.4 Time-Delayed Cascading Failure Model in Interdependent Networks

Infrastructure is modeled as interdependent multi-layer networks: power layer Gp = (P, Ep) with M substations, and communication layer Gc = (C, Ec) with N base stations. Each communication node depends on one upstream power node via network-distance-based mapping: fdep(ci) = argmin Dist_G(ci, pj) (Eq. 13).

**Flood-induced physical failure.** For substation pj, the local flood depth Wp(pj,t) triggers failure by threshold: Sp(pj,t) = 1 if Wp ≤ Wth, else 0 (Eq. 14), with Wth = 0.5 m. Physical damage is irreversible without restoration.

**Time-delayed propagation via backup energy.** Communication nodes carry backup batteries B(ci,0) ~ U(3, 5) h. When the upstream power node fails, the battery depletes: B(ci,t+Δt) = max[0, B(ci,t) − λ(1 − Sp(fdep(ci),t))Δt] (Eq. 15). The node fails when B = 0. This introduces a temporal buffer between physical damage and functional failure — delayed cascading.

### 3.5 Dynamic Restoration Optimization under Flood-Constrained Transportation

**Dynamic road network.** Road segments are blocked when flood depth at their center exceeds Wroad = 0.3 m: L(u,v,t) = L0 if Wr ≤ Wroad, else ∞ (Eq. 16).

**Multi-objective restoration priority.** The utility of restoring substation pj is U(pj,t) = Σ Sc(ci,t)·(1 + γ/(B(ci,t) + ε)) (Eq. 17), balancing the number of dependent surviving stations (base term 1) and urgency (1/B term with urgency weight γ = 5). The target is p\* = argmax U(pj,t).

**Routing and restoration.** Fleets compute Dijkstra shortest paths on the dynamic graph: Π\*(t) = argmin Σ L(u,v,t) (Eq. 18). Upon arrival, Sp(p\*,t_arrive) → 1, immediately stopping battery depletion of dependent nodes.

### 3.6 Simulation Workflow

**Algorithm 1: High-resolution urban resilience digital twin simulation**

1. Initialize terrain elevation, drainage parameters, and infrastructure networks
2. For each simulation timestep t:
   - Update rainfall forcing
   - Calculate CA-based flood propagation
   - Update drainage storage saturation
   - Evaluate power infrastructure flooding damage
   - Update communication battery depletion
   - Calculate system resilience indicator Φ(t) = (1/N)ΣSc(ci,t)
   - If failed infrastructure exists: compute restoration priorities, update dynamic road accessibility, generate optimal repair routes, execute restoration actions
3. Output flood evolution and resilience trajectories

## 4. Case Study and Experimental Design

### 4.1 Study Area

Miyazaki City, located on the southeastern coast of Kyushu Island, Japan, is frequently affected by typhoon-induced extreme precipitation events. The urban area is characterized by heterogeneous terrain: elevated mountainous regions in the west and relatively flat low-elevation plains near the Pacific coastline. The Oyodo River system crosses the urban area, creating complex surface runoff patterns and flood accumulation zones.

### 4.2 Digital Twin Environment Construction

The physical environment was reconstructed from open elevation data (Open-Meteo API); the road network within a 3 km radius of the city center was extracted from OpenStreetMap and projected to EPSG:6674. The study region was discretized into a 650×650 cell domain (422,500 cells), each containing elevation, surface water depth, drainage capacity, and subsurface storage state. Two infrastructure layers were deployed: M = 15 power substations and N = 40 communication base stations, with network-distance-based dependency mapping.

**Table 1. Data sources used in the digital twin framework**

| Dataset | Purpose | Model component |
|---|---|---|
| Open-Meteo elevation API | Terrain reconstruction and slope | Flood model |
| OpenStreetMap road network | Topology and accessibility | Network model |
| Infrastructure deployment | Component failure analysis | Cascading failure model |
| Synthetic rainfall scenario | Hazard forcing | Flood model |
| Recovery parameters | Emergency response | Restoration optimization |

### 4.3 Extreme Rainfall Scenario

An extreme rainfall event of T = 8 h was simulated with a modified Chicago design storm profile R(t) = R_base + R_peak·sin(πt/T) (Eq. 19), peak intensity 100 mm/h, cumulative precipitation ≈ 567 mm. The time axis was discretized into 24 frames, each containing 30 CA sub-steps of Δt = 10 s.

**Table 2. Main simulation parameters**

| Category | Parameter | Value |
|---|---|---|
| Spatial resolution | Grid size | 650 × 650 |
| Flood model | Cell number | 422,500 |
| Rainfall | Duration / peak | 8 h / 100 mm/h |
| Infrastructure | Substations / stations | 15 / 40 |
| Flood threshold | Substation damage | 0.5 m |
| Transportation | Road blockage | 0.3 m |
| Battery | Backup duration | 3–5 h |
| Restoration | Fleets / speed / repair time | 2 / 30 km/h / 1 h |

### 4.4 Experimental Scenarios and Evaluation Metrics

Four scenarios were designed: **S1** normal rainfall (baseline behavior); **S2** extreme flood (main scenario); **S3** cascading failure activation; **S4** adaptive restoration comparison. Two baselines were defined:

- **Baseline 1 (static bathtub flood):** the CA flood model is replaced by a spatially uniform accumulation model with the drainage coefficient fixed at the median of the heterogeneous drainage field.
- **Baseline 2 (no restoration):** all mechanisms are preserved but emergency dispatch is removed (0 fleets).

Evaluation indicators: (i) flood extent and depth distribution; (ii) resilience index Φ(t) and its time integral (AUC); (iii) recovery time (first time Φ(t) returns to 95% of its initial value); (iv) infrastructure availability curves.

## 5. Results and Performance Evaluation

### 5.1 Study Area and Infrastructure Deployment

Fig. 1 shows the reconstructed terrain of the study area together with the OSM road network and the deployed infrastructure. The western mountainous region and the eastern coastal plain are clearly distinguished, providing a heterogeneous physical basis for flood propagation.

**Fig. 1.** Study area (Miyazaki City): reconstructed terrain, road network, power substations (red squares) and communication base stations (cyan diamonds). *(figures/fig1_study_area.png)*

### 5.2 Nonlinear Flood Evolution and Drainage Saturation

Fig. 2 shows three snapshots of the flood depth field (early buffer stage, peak rainfall stage, and late recession stage).

**Fig. 2.** Spatial evolution of flood depth at different simulation stages. *(figures/fig2_flood_evolution.png)*

**Stage I — hydrological buffer period.** During the first ~2 h, the maximum depth grew from 0 to about 1.5 m while drainage systems absorbed most incoming water — a temporary resilience buffer before saturation.

**Stage II — drainage saturation transition.** Between 2 and 4 h, subsurface storage was gradually exhausted (K → 0), drainage effectiveness declined, and the maximum depth accelerated from 2.8 m (t = 1 h) to 12.6 m (t = 4 h). Flood growth is not proportional to rainfall input once drainage capacity is exhausted — a critical hydrological tipping point.

**Stage III — rapid surface flood expansion.** After saturation, surface hydraulic exchange dominated and the peak depth reached 16.59 m before slowly receding. Water preferentially accumulated in low-elevation regions and river-adjacent areas.

### 5.3 Comparison with the Static Flood Model

**Table 3. Summary metrics of the main scenario and baselines**

| Scenario | Peak depth (m) | Flooded subst. (max) | Restored subst. (final) | Failed comm. (max) |
|---|---|---|---|---|
| Proposed framework | 16.59 | 1 | 2 | 1 |
| Baseline 1 (static flood) | 0.48 | 0 | 0 | 0 |
| Baseline 2 (no restoration) | 16.59 | 3 | 0 | 10 |

The static bathtub model produces a peak depth of only 0.48 m and floods no substation, whereas the proposed CA model reaches 16.59 m and exposes up to three substations — an underestimation of more than 97%. Spatially homogeneous flood assumptions substantially underestimate localized infrastructure exposure in heterogeneous urban environments.

### 5.4 Time-Delayed Cascading Failure Analysis

The first substation was flooded at approximately t = 2 h; thanks to the backup-battery buffer, no communication station failed during the first 6 h. Three characteristic phases were observed: physical damage accumulation → battery-supported buffering → accelerated communication failure after battery depletion. In the no-restoration baseline, communication failures emerged at t ≈ 6.7 h and grew to ten stations by the end of the event. Temporal redundancy significantly influences the observed failure trajectory.

### 5.5 Effectiveness of the Dynamic Restoration Strategy

Fig. 3 shows the resilience trajectories Φ(t) of the three scenarios. Without restoration, the communication network degraded to Φ = 0.75 with ten failed stations. With dynamic dispatch, both fleets restored two flooded substations within the first 3.3 h, limiting failures to a single station (Φ ≥ 0.975 throughout) and improving the resilience AUC from 0.951 to 0.996.

**Fig. 3.** Communication network resilience trajectories Φ(t) of the proposed framework and the two baselines. *(figures/fig3_resilience_curves.png)*

### 5.6 Sensitivity Analysis

**Fig. 4.** One-at-a-time sensitivity analysis. *(figures/fig4_sensitivity.png)*

- **Rainfall intensity:** 70 → 100 → 130 mm/h raises the peak depth from 15.14 → 16.59 → 19.91 m (~31% depth increase for a 30% rainfall increase at the highest level).
- **Drainage capacity:** once subsurface storage is exhausted during the peak, increasing the drainage rate no longer reduces the peak depth (16.59 m in all configurations) — confirming that storage saturation, not the drainage rate, governs peak flooding under extreme rainfall.
- **Backup-battery duration:** shortening to 1.5–2.5 h reduces the resilience AUC from 0.996 to 0.989; extending to 6–8 h completely prevents communication failures (Φ = 1.0 throughout).
- **Repair fleets:** two fleets suffice for the damage scenario considered; a single fleet briefly exposes a second substation before it is repaired.

Rainfall intensity and backup-battery duration are the dominant factors controlling resilience performance under the simulated event.

### 5.7 Summary of Results

The proposed framework simultaneously represents flood dynamics, infrastructure cascading failures, and adaptive recovery processes. The integration of physics-based simulation and decision optimization provides a comprehensive approach for evaluating urban resilience under extreme flooding scenarios.

## 6. Discussion

### 6.1 Implications for Urban Resilience Planning

Urban resilience is determined not only by the physical robustness of infrastructure components but also by the temporal characteristics of failure propagation and recovery capability. First, flood resilience cannot be evaluated solely from rainfall intensity or static elevation information: drainage capacity, terrain heterogeneity, and local accumulation processes must be incorporated [12, 13]. Second, operational redundancy (backup batteries, distributed power resources) significantly extends the functional lifetime of dependent infrastructure, but it is a temporary buffer rather than a permanent solution — delayed failure postpones, but does not eliminate, collapse [15]. Third, emergency response efficiency depends on both infrastructure priority and transportation accessibility [19]; static geographic-distance strategies become ineffective when transportation networks are dynamically disrupted by flooding.

### 6.2 Contribution to Digital Twin-Based Disaster Management

Many existing digital twins focus on monitoring and visualization rather than predictive resilience analysis [17, 16]. The proposed framework extends the concept with (i) physics-informed environmental evolution, (ii) multi-layer infrastructure failure simulation, and (iii) closed-loop human intervention modeling — enabling the digital twin to function as a decision-support system for disaster mitigation and recovery.

### 6.3 Model Limitations and Future Work

- **Hydrodynamic approximation.** The CA model does not fully reproduce momentum conservation, turbulence, and complex urban obstacles; the conservative CFL parameter (α = 0.12) limits flow propagation speed, so reported absolute times represent model time rather than real physical time. Future work: adaptive mesh refinement, adaptive time stepping, or hybrid CA–SWE approaches [12].
- **Infrastructure representation.** Only power and communication dependencies are modeled; future extensions should include transportation, water supply, healthcare, and distributed energy resources with self-healing islanding [5].
- **Parameter calibration and validation.** Parameters derive from engineering assumptions; validation against historical flood observations (e.g., IoU between simulated and observed inundation areas) is required.
- **Human decision modeling.** Algorithmic dispatch is a simplification of human decision-making, resource constraints, and institutional coordination [22]; agent-based models are a promising extension.
- **Deployment randomness.** Infrastructure deployment follows a fixed random seed; multi-seed Monte Carlo averaging is planned to quantify deployment uncertainty.

## 7. Conclusion

This study proposed a high-resolution digital twin framework for evaluating urban infrastructure resilience under extreme flooding scenarios, integrating terrain-informed CA flood propagation, time-delayed cascading failure mechanisms, and dynamic restoration optimization. The main findings are:

1. **Flood evolution exhibits nonlinear transition behavior.** The interaction of rainfall input, heterogeneous terrain, and drainage saturation produces critical transition points where flooding rapidly changes from a manageable condition to severe surface accumulation.
2. **Temporal redundancy strongly influences cascading failure dynamics.** Backup energy introduces a delay between physical damage and functional disruption; ignoring this mechanism leads to inaccurate resilience estimation.
3. **Adaptive restoration improves system-level resilience.** Dynamic dispatch considering infrastructure importance and flood-constrained accessibility effectively reduces cascading impacts and improves recovery outcomes under limited emergency resources.

Methodologically, the framework bridges physical flood dynamics, infrastructure dependency modeling, and recovery optimization within a unified computational environment. Practically, it provides evidence-based support for resilience planning by identifying critical vulnerabilities, evaluating cascading impacts, and testing adaptive intervention strategies. The proposed approach provides a foundation for future intelligent disaster management systems that combine physical simulation, network science, and adaptive decision-making.

---

## Data Availability

The input data used in this study are derived from publicly available third-party sources: the road network of Miyazaki City was obtained from OpenStreetMap (OSM, https://www.openstreetmap.org), and terrain elevation data were retrieved from the Open-Meteo elevation API (https://open-meteo.com). No proprietary or confidential data were used.

The complete simulation framework, including the terrain-informed cellular flood model, the interdependent infrastructure failure model, the adaptive restoration optimizer, and the visualization modules, is implemented in Python. All source code, configuration files, cached input data, and the full set of experimental outputs (frame-wise simulation trajectories, summary metrics, and figure-generation scripts) are publicly available in the repository https://github.com/mozhu-cn/urban-resilience-digital-twin. The entire experimental pipeline, including the main scenario, the two baseline scenarios, and the one-at-a-time sensitivity analysis, is fully reproducible by executing the provided scripts with the released code and data.

---

## References

1. IPCC, *Managing the Risks of Extreme Events and Disasters to Advance Climate Change Adaptation (SREX)*, Cambridge University Press, 2012.
2. S. M. Rinaldi, J. P. Peerenboom, T. K. Kelly, Identifying, understanding, and analyzing critical infrastructure interdependencies, *IEEE Control Systems Magazine* 21(6) (2001) 11–25.
3. S. V. Buldyrev, R. Parshani, G. Paul, H. E. Stanley, S. Havlin, Catastrophic cascade of failures in interdependent networks, *Nature* 464 (2010) 1025–1028.
4. J. Gao, S. V. Buldyrev, S. Havlin, H. E. Stanley, Robustness of a network of networks, *Physical Review Letters* 107 (2011) 195701.
5. M. Ouyang, Review on modeling and simulation of interdependent critical infrastructure systems, *Reliability Engineering & System Safety* 121 (2014) 43–60.
6. M. Ouyang, L. Dueñas-Osorio, X. Min, A three-stage resilience analysis framework for urban infrastructure systems, *Structural Safety* 36–37 (2012) 23–31.
7. M. Bruneau et al., A framework to quantitatively assess and enhance the seismic resilience of communities, *Earthquake Spectra* 19(4) (2003) 733–752.
8. S. E. Chang, M. Shinozuka, Measuring improvements in the disaster resilience of communities, *Earthquake Spectra* 20(3) (2004) 739–755.
9. R. Albert, A.-L. Barabási, Statistical mechanics of complex networks, *Reviews of Modern Physics* 74 (2002) 47–97.
10. M. E. J. Newman, The structure and function of complex networks, *SIAM Review* 45(2) (2003) 167–256.
11. M. Ouyang, L. Dueñas-Osorio, Time-dependent resilience assessment and improvement of urban infrastructure systems, *Chaos* 22(3) (2012) 033122.
12. P. D. Bates, M. S. Horritt, T. J. Fewtrell, A simple inertial formulation of the shallow water equations for efficient two-dimensional flood inundation modelling, *Journal of Hydrology* 387(1–2) (2010) 33–45.
13. M. Guidolin et al., A weighted cellular automata 2D inundation model for rapid flood analysis, *Environmental Modelling & Software* 84 (2016) 378–394.
14. B. Ghimire et al., Formulation of a fast 2D urban pluvial flood model using a cellular automata approach, *Journal of Hydroinformatics* 15(3) (2013) 676–686.
15. M. Panteli, P. Mancarella, The Grid: stronger, bigger, smarter?, *IEEE Power and Energy Magazine* 13(3) (2015) 58–66.
16. M. Batty, Digital twins, *Environment and Planning B: Urban Analytics and City Science* 45(5) (2018) 817–820.
17. M. Grieves, J. Vickers, Digital twin: mitigating unpredictable, undesirable emergent behavior in complex systems, in: *Transdisciplinary Perspectives on Complex Systems*, Springer, 2017, pp. 85–113.
18. F. Tao, H. Zhang, A. Liu, A. Y. C. Nee, Digital twin in industry: state-of-the-art, *IEEE Transactions on Industrial Informatics* 15(4) (2019) 2405–2415.
19. G. Laporte, Fifty years of vehicle routing, *Transportation Science* 43(4) (2009) 408–416.
20. M. Issermann, F.-J. Chang, H. Jia, Efficient urban inundation model for live flood forecasting with cellular automata and motion cost fields, *Water* 12(7) (2020) 1997.
21. C. S. Holling, Resilience and stability of ecological systems, *Annual Review of Ecology and Systematics* 4 (1973) 1–23.
22. G. Di Baldassarre et al., Socio-hydrology: conceptualising human-flood interactions, *Hydrology and Earth System Sciences* 17(8) (2013) 3295–3303.
23. M. Haklay, P. Weber, OpenStreetMap: user-generated street maps, *IEEE Pervasive Computing* 7(4) (2008) 12–18.
