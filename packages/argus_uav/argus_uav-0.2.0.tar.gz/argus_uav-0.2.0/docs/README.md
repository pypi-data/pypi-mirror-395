# Argus Documentation

**Complete documentation for the UAV Remote ID Spoofing Defense System.**

---

## 📚 **Documentation Index**

### **Getting Started**

1. **[CLI.md](CLI.md)** - Main CLI tool guide (Recommended starting point!)

   - Interactive and command-line modes
   - All attacks and detection methods
   - Live visualization and performance comparison
   - Usage examples and best practices

2. **[QUICKSTART.md](QUICKSTART.md)** - Get up and running in 10 minutes

   - Installation instructions
   - Quick examples
   - Common tasks

3. **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Solutions to common issues
   - Visualization problems (Wayland, PySide6/Qt)
   - Import errors
   - Performance issues
   - Test and lint problems

### **Technical Documentation**

4. **[algorithm_details.md](algorithm_details.md)** - Deep dive into algorithms

   - Graph-theoretic detection (spectral, centrality)
   - Cryptographic defenses (Ed25519)
   - Machine learning (Node2Vec, isolation forest)
   - Consensus algorithms
   - Performance complexity analysis

5. **[data_formats.md](data_formats.md)** - Data structures and formats

   - Remote ID message format
   - Configuration files (YAML)
   - Results files (JSON)
   - Graph snapshots (pickle)
   - Visualization outputs
   - Type definitions

6. **[references.md](references.md)** - Research papers and citations
   - Graph theory papers
   - Cryptography standards
   - UAV Remote ID regulations
   - Security research
   - Software libraries

### **Project Documentation**

7. **[STATUS.md](STATUS.md)** - Complete project status

   - All features and completion summary
   - Performance benchmarks
   - Scalability results
   - Research contributions
   - Quick usage guide

8. **[ORIGINAL_PROPOSAL.md](ORIGINAL_PROPOSAL.md)** - Original project proposal
   - Research description
   - Timeline
   - Expected deliverables
   - Risks and extensions

---

## 🎯 **Quick Navigation**

### **I want to...**

**...use the CLI tool (recommended!)**  
→ Read [CLI.md](CLI.md)

**...get started quickly**  
→ Read [QUICKSTART.md](QUICKSTART.md)

**...fix problems or errors**  
→ Read [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

**...understand the algorithms**  
→ Read [algorithm_details.md](algorithm_details.md)

**...see what data formats are used**  
→ Read [data_formats.md](data_formats.md)

**...find research papers**  
→ Read [references.md](references.md)

**...check project status and completion**  
→ Read [STATUS.md](STATUS.md)

**...review original proposal**  
→ Read [ORIGINAL_PROPOSAL.md](ORIGINAL_PROPOSAL.md)

---

## 📖 **Documentation Structure**

```
docs/
├── README.md                    # This file (documentation index)
├── CLI.md                       # Main CLI tool guide
├── QUICKSTART.md                # Getting started guide
├── TROUBLESHOOTING.md           # Solutions to common problems
├── algorithm_details.md         # Technical algorithm documentation
├── data_formats.md              # Data structure specifications
├── references.md                # Research paper citations
├── STATUS.md                    # Project status & completion
└── ORIGINAL_PROPOSAL.md         # Original research proposal
```

---

## 🔗 **External Resources**

**Main README**: [../README.md](../README.md) - Project overview and installation

**Examples**: [../examples/](../examples/) - Runnable demonstrations  
**CLI Tool**: Use `argus` command after installation

**Tests**: [../tests/](../tests/) - Unit and integration tests

---

## 📝 **For Developers**

If you're contributing to Argus or extending it:

1. Start with [algorithm_details.md](algorithm_details.md) to understand the theory
2. Check [data_formats.md](data_formats.md) for data structures
3. Review module docstrings in `argus/` for API details
4. Examine tests in `tests/` for usage examples
5. Run examples in `examples/` to see features in action

---

## 📄 **For Researchers**

If you're using Argus for research:

1. Use [CLI.md](CLI.md) to run experiments and generate results
2. Read [QUICKSTART.md](QUICKSTART.md) to get running quickly
3. Check [algorithm_details.md](algorithm_details.md) for methodology
4. Use [references.md](references.md) for citations
5. Review [STATUS.md](STATUS.md) for capabilities

---

## 🎓 **Academic Use**

### **Citing Argus**

If you use this system in your research, please cite:

```bibtex
@inproceedings{argus2025,
  author = {Xing, Sang and Niure Kandel, Laxima},
  title = {Cryptographic Authentication for UAV Swarm Security: A Comparative Analysis of Detection Methods Against Spoofing Attacks},
  year = {2025},
  institution = {Embry-Riddle Aeronautical University},
  url = {https://github.com/Sang-Buster/Argus}
}
```

### **Related Papers**

See [references.md](references.md) for a complete list of 19 research papers that informed this work.

---

## 📞 **Support**

- **Using the CLI?** See [CLI.md](CLI.md)
- **Questions?** Check [QUICKSTART.md](QUICKSTART.md) first
- **Issues?** See [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **Research?** Review [algorithm_details.md](algorithm_details.md)
- **Citations?** Check [references.md](references.md)

---

**Last Updated**: December 2025  
**Documentation Version**: 0.2.0
