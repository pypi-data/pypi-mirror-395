# References

Research papers and standards cited in Argus development.

## Graph Theory and Spectral Analysis

1. **Peel, L., Delvenne, J. C., & Lambiotte, R. (2015)**  
   "Detecting Change Points in the Large-scale Structure of Evolving Networks"  
   _arXiv preprint arXiv:1403.0989_

   - Spectral methods for temporal network analysis
   - Laplacian eigenvalue monitoring
   - Change point detection in dynamic graphs

2. **Fiedler, M. (1973)**  
   "Algebraic connectivity of graphs"  
   _Czechoslovak Mathematical Journal_

   - Introduced algebraic connectivity (second eigenvalue)
   - Relationship to graph robustness
   - Spectral partitioning methods

3. **Chung, F. R. (1997)**  
   "Spectral Graph Theory"  
   _American Mathematical Society_
   - Comprehensive treatment of graph spectra
   - Applications to network analysis
   - Eigenvalue bounds and perturbation theory

## Centrality and Network Analysis

4. **Freeman, L. C. (1978)**  
   "Centrality in social networks conceptual clarification"  
   _Social Networks, 1(3), 215-239_

   - Degree, betweenness, and closeness centrality
   - Theoretical foundations
   - Applications to network structure

5. **Newman, M. E. (2010)**  
   "Networks: An Introduction"  
   _Oxford University Press_
   - Comprehensive network science textbook
   - Centrality measures
   - Community detection
   - Random graph models

## Consensus Algorithms

6. **Olfati-Saber, R., & Murray, R. M. (2004)**  
   "Consensus Problems in Networks of Agents with Switching Topology and Delays"  
   _IEEE Transactions on Automatic Control, 49(9), 1520-1533_

   - Average consensus algorithm
   - Convergence analysis
   - Networked multi-agent systems

7. **Ren, W., & Beard, R. W. (2008)**  
   "Distributed Consensus in Multi-vehicle Cooperative Control"  
   _Springer_
   - UAV swarm coordination
   - Consensus protocols
   - Applications to formation control

## Machine Learning and Anomaly Detection

8. **Grover, A., & Leskovec, J. (2016)**  
   "node2vec: Scalable Feature Learning for Networks"  
   _Proceedings of the 22nd ACM SIGKDD_

   - Graph embedding algorithm
   - Random walk strategies
   - Applications to node classification

9. **Liu, F. T., Ting, K. M., & Zhou, Z. H. (2008)**  
   "Isolation Forest"  
   _Proceedings of the 8th IEEE International Conference on Data Mining_

   - Unsupervised anomaly detection
   - Tree-based ensemble method
   - Isolation depth scoring

10. **Perozzi, B., Al-Rfou, R., & Skiena, S. (2014)**  
    "DeepWalk: Online Learning of Social Representations"  
    _Proceedings of the 20th ACM SIGKDD_
    - Precursor to Node2Vec
    - Graph embeddings via random walks
    - Skip-gram model for graphs

## Cryptography

11. **Bernstein, D. J., Duif, N., Lange, T., Schwabe, P., & Yang, B. Y. (2012)**  
    "High-speed high-security signatures"  
    _Journal of Cryptographic Engineering, 2(2), 77-89_

    - Ed25519 signature scheme
    - Curve25519 elliptic curve
    - Performance benchmarks
    - Security analysis

12. **Josefsson, S., & Liusvaara, I. (2017)**  
    "Edwards-Curve Digital Signature Algorithm (EdDSA)"  
    _RFC 8032_
    - Official EdDSA specification
    - Ed25519 and Ed448 variants
    - Test vectors and implementation guidance

## UAV Remote ID Standards

13. **FAA (2021)**  
    "Remote Identification of Unmanned Aircraft"  
    _14 CFR Part 89_

    - Federal regulation mandating Remote ID
    - Message format requirements
    - Broadcast frequency specifications
    - Compliance timeline

14. **ASTM International (2020)**  
    "Standard Specification for Remote ID and Tracking"  
    _ASTM F3411-19_
    - Technical standard for Remote ID
    - Data element specifications
    - Performance requirements
    - Test procedures

## UAV Security and Spoofing

15. **Humphreys, T. E., et al. (2008)**  
    "Assessing the Spoofing Threat: Development of a Portable GPS Civilian Spoofer"  
    _Proceedings of the ION GNSS International Technical Meeting_

    - GPS spoofing methodology
    - Attack demonstrations
    - Vulnerability analysis

16. **Manesh, M. R., & Kaabouch, N. (2019)**  
    "Analysis of vulnerabilities, attacks, countermeasures and overall risk of the Automatic Dependent Surveillance-Broadcast (ADS-B) system"  
    _International Journal of Critical Infrastructure Protection, 25, 37-55_

    - Similar broadcast-based identification system
    - Attack taxonomy
    - Defense mechanisms

17. **Ferreira, R., et al. (2020)**  
    "A Survey on Attacks and Defense Mechanisms for Unmanned Aerial Vehicles"  
    _IEEE Access, 8, 141337-141360_
    - Comprehensive UAV security survey
    - Attack vectors
    - Defense strategies

## Graph Anomaly Detection

18. **Akoglu, L., Tong, H., & Koutra, D. (2015)**  
    "Graph based anomaly detection and description: a survey"  
    _Data Mining and Knowledge Discovery, 29(3), 626-688_

    - Survey of graph anomaly detection methods
    - Taxonomy of techniques
    - Applications and benchmarks

19. **Ranshous, S., et al. (2015)**  
    "Anomaly detection in dynamic networks: a survey"  
    _Wiley Interdisciplinary Reviews: Computational Statistics, 7(3), 223-247_
    - Temporal graph analysis
    - Dynamic anomaly detection
    - Streaming graph algorithms

## Additional Resources

### Software Libraries

- **NetworkX**: https://networkx.org/

  - Python graph library documentation
  - Algorithm implementations
  - Tutorials and examples

- **PyCryptodome**: https://www.pycryptodome.org/

  - Cryptographic primitives
  - Ed25519 implementation
  - Usage examples

- **scikit-learn**: https://scikit-learn.org/
  - Machine learning library
  - Isolation Forest documentation
  - Best practices

### Datasets (Future Work)

- **OpenSky Network**: https://opensky-network.org/

  - Real ADS-B aircraft tracking data
  - Can be adapted for Remote ID research
  - Historical and live data

- **Remote ID GitHub Repositories**:
  - DroneID: https://github.com/opendroneid
  - Reference implementations
  - Test data and tools

### Related Projects

- **gr-adsb**: GNU Radio ADS-B receiver
- **dump1090**: ADS-B decoder (similar to Remote ID)
- **rtl-sdr**: Software Defined Radio tools

## Citation

If you use Argus in your research, please cite:

```bibtex
@inproceedings{argus2025,
  author = {Xing, Sang and Niure Kandel, Laxima},
  title = {Cryptographic Authentication for UAV Swarm Security: A Comparative Analysis of Detection Methods Against Spoofing Attacks},
  year = {2025},
  institution = {Embry-Riddle Aeronautical University},
  url = {https://github.com/Sang-Buster/Argus}
}
```

## License

Argus is released under the MIT License. See LICENSE file for details.

All referenced papers and standards are copyright their respective authors and publishers.
