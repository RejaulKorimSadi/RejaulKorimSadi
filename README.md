<a href="https://github.com/RejaulKorimSadi">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/hero-dark.svg">
    <img src="assets/hero-light.svg" alt="Md Rejaul Korim Sadi, AI researcher. Artificial Intelligence | NLP | Research | AI Business Solutions. Why does a language model sound certain when it is wrong?" width="100%">
  </picture>
</a>

<br>

I study why large language models state false things in the same confident tone they use for the truth. My B.Sc. thesis, *MRI of a Mad Machine: The Structural Origins of Hallucination*, traces those errors to three design choices inside the transformer and tests each one with pre-registered experiments, independent raters and open data. Alongside it, I am asking whether living neurons could one day hold part of a language model's context.

<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/s1-dark.svg">
  <img src="assets/s1-light.svg" alt="01. Three ways to be wrong" width="100%">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/mechanisms-dark.svg">
  <img src="assets/mechanisms-light.svg" alt="Three mechanisms: self-attention favours association over truth, the training objective favours the probable over the true, and decoding commits before it can check. Data amplifies all three but creates none of them." width="100%">
</picture>

<br><br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/s2-dark.svg">
  <img src="assets/s2-light.svg" alt="02. The evidence" width="100%">
</picture>

<p align="center">
<a href="https://github.com/RejaulKorimSadi/P3-Commitment-Hallucination-Test"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/ev-p3-dark.svg"><img src="assets/ev-p3-light.svg" alt="The Commitment Test: repairing a model's first wrong fact cut answers with a later error from 92.5% to 48.1% (n = 106), yet the models knew that fact alone on only 2 of 111 items." width="49%"></picture></a> <a href="https://github.com/RejaulKorimSadi/The-Attention-Ablation-Test"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/ev-p5-dark.svg"><img src="assets/ev-p5-light.svg" alt="The Attention Ablation Test: at 2.8B, the attention model repeated a planted falsehood on 650 of 666 items against 566 for its matched state-space model." width="49%"></picture></a>
</p>
<p align="center">
<a href="https://github.com/Taseen06/R2"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/ev-r2-dark.svg"><img src="assets/ev-r2-light.svg" alt="Wrong with Confidence: removing a question's key detail raised error from 39.1% to 52.0%, and 75.3% of wrong answers carried no hedge." width="49%"></picture></a> <a href="https://github.com/Taseen06/R3-LLM-Rating"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/ev-r3-dark.svg"><img src="assets/ev-r3-light.svg" alt="Models as judges: across 270,000 ratings of 15,000 screens, low agreement with a heuristic scorer is mostly a constant, correctable offset." width="49%"></picture></a>
</p>

<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/s3-dark.svg">
  <img src="assets/s3-light.svg" alt="03. Now: neurons, meet language models" width="100%">
</picture>

<a href="https://github.com/RejaulKorimSadi/Wetware-LLM-in-Silico">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/wetware-dark.svg">
    <img src="assets/wetware-light.svg" alt="The Cellular Data Center: text is encoded as stimulation, simulated living neurons hold the context, and a trained readout predicts the next token. In the pilot, a silicon network of the same size won every task." width="100%">
  </picture>
</a>

<br><br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/s4-dark.svg">
  <img src="assets/s4-light.svg" alt="04. Papers" width="100%">
</picture>

| | Paper | Status |
|:--|:--|:--|
| **R1** | **From Architecture to Output: Testing the Structural Origins of Hallucination and the Amplifying Role of Data**<br>Sadi, Tasin, Naeem · [arXiv:2606.07537](https://arxiv.org/abs/2606.07537) · [code](https://github.com/RejaulKorimSadi/From_Architecture_to_Output_R1_Empirical_Evidence) | Under review, *Northern European Journal of Language Technology* |
| **R2** | **Wrong with Confidence: Measuring Hallucination, Overconfidence and Identity-Conditioned Behaviour in Large Language Models**<br>Sadi, Tasin, Naeem, D. F. Chowdhury, H. A. A. Chowdhury · [pre-registration](https://doi.org/10.17605/OSF.IO/CS967) · [data](https://doi.org/10.5281/zenodo.20677241) · [code](https://github.com/Taseen06/R2) | Under review, *PeerJ Computer Science* |
| **R3** | **Characterising Divergence Between Heuristic and Language-Model Ratings of Mobile User Interface Quality**<br>Sadi, Naeem, Tasin, Moosa, Emon, Rashid, Ahmed · [arXiv:2609.05423](https://arxiv.org/abs/2609.05423) · [code](https://github.com/Taseen06/R3-LLM-Rating) · earlier version presented at EFAST 2026 | Under review, *PeerJ Computer Science* |
| **AJSE** | **Behavioral Differences Between Active and Inactive Users in Competitive Programming: A Rating-Restricted Analysis of Codeforces Activity**<br>Ruhan, Sadi, Rafi, D. F. Chowdhury, Opi, Mim, Naeem · [arXiv:2608.28618](https://arxiv.org/abs/2608.28618) | Accepted, *AIUB Journal of Science and Engineering* |
| **Preprint** | **The Cellular Data Center**<br>Sadi, Ruhan, Chowdhury · [code](https://github.com/RejaulKorimSadi/Wetware-LLM-in-Silico) | In preparation |

<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/s5-dark.svg">
  <img src="assets/s5-light.svg" alt="05. Instruments" width="100%">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/instruments-dark.svg">
  <img src="assets/instruments-light.svg" alt="Languages: Python, C, C++, Google Apps Script. ML and NLP: PyTorch, Hugging Face Transformers, local LLM inference on consumer GPUs, prompt and evaluation design. Research methods: pre-registration (OSF), independent annotation, Cohen's kappa, McNemar and chi-squared tests, reproducible pipelines. Tools: Git and GitHub, LaTeX, Google Sheets, workflow automation." width="100%">
</picture>

Outside research, I build applied AI systems: for IntelliGency Solutions (US) I designed a lead engine in which a language model drafts each message and a person approves it before it is sent.

<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/s6-dark.svg">
  <img src="assets/s6-light.svg" alt="06. Signal" width="100%">
</picture>

<p align="center">
<picture><source media="(prefers-color-scheme: dark)" srcset="assets/stats-dark.svg"><img src="assets/stats-light.svg" alt="GitHub activity over the last 12 months, updated daily" width="49%"></picture> <picture><source media="(prefers-color-scheme: dark)" srcset="assets/languages-dark.svg"><img src="assets/languages-light.svg" alt="Languages across my public repositories, updated daily" width="49%"></picture>
</p>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/RejaulKorimSadi/RejaulKorimSadi/output/snake-dark.svg">
  <img src="https://raw.githubusercontent.com/RejaulKorimSadi/RejaulKorimSadi/output/snake-light.svg" alt="Contribution graph animation" width="100%">
</picture>

<br><br>

<p align="center">
<a href="mailto:rejaulkorimsadi@gmail.com"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/btn-email-dark.svg"><img src="assets/btn-email-light.svg" alt="Email: rejaulkorimsadi@gmail.com" width="49%"></picture></a> <a href="https://www.linkedin.com/in/rejaulkorimsadi"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/btn-linkedin-dark.svg"><img src="assets/btn-linkedin-light.svg" alt="LinkedIn: in/rejaulkorimsadi" width="49%"></picture></a>
</p>
<p align="center">
<a href="https://orcid.org/0009-0004-1116-2985"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/btn-orcid-dark.svg"><img src="assets/btn-orcid-light.svg" alt="ORCID: 0009-0004-1116-2985" width="49%"></picture></a> <a href="https://arxiv.org/search/?searchtype=author&query=Rejaul+Korim+Sadi"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/btn-arxiv-dark.svg"><img src="assets/btn-arxiv-light.svg" alt="arXiv papers" width="49%"></picture></a>
</p>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/footer-dark.svg">
  <img src="assets/footer-light.svg" alt="Open to research collaboration on reliable language models. Sylhet, Bangladesh." width="100%">
</picture>
