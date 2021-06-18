# VeRoViz: Vehicle Routing Visualization

[![PyPI version](https://img.shields.io/pypi/v/veroviz.svg?style=flat)](https://pypi.org/project/veroviz/) [![License](https://img.shields.io/pypi/l/veroviz.svg?style=flat)](https://pypi.org/project/veroviz/)

VeRoViz is a suite of tools (primarily written in Python) to easily generate, test, and visualize vehicle routing problems.

Key features of the Python tools include:
- Generation of nodes on road networks;
- Calculation of travel time/distance matrices using external data providers;
- Creation of Leaflet maps to view nodes, routes, and basic geometric shapes; and
- Generation of dynamic CesiumJS content to view 4D "movies" of vehicle routing problems.


All Python source code is hosted in this repository.  Documentation, examples, contact information are available from the [VeRoViz project website](https://veroviz.org).

---

## About VeRoViz
VeRoViz is an open-source project from the Optimator Lab, in the University at Buffalo's Department of Industrial & Systems Engineering.

This project began in 2018 as a tool for our [research lab](https://optimatorlab.org). It is under ongoing development.

The prototypical VeRoViz user is someone who is developing models, algorithms, or heuristics for a vehicle routing problem (entities that move between locations). [Sketch](https://veroviz.org/sketch.html) can also be used as a teaching tool in the classroom to introduce vehicle routing concepts.

The aim of VeRoViz is to help such a user
- obtain road network data,
- sketch the locations of nodes (e.g., customers and depots),
- visualize arcs (connections) among these nodes,
- generate 3D movies showcasing solutions to vehicle routing problems,
- quickly generate test problems and distance (and/or time) matrices.

VeRoViz is not an optimization package. If you're interested in vehicle routing solvers, you might consider [GraphHopper](https://graphhopper.com/), [Vroom](https://vroom-project.org/), [OR-Tools](https://developers.google.com/optimization/routing/vrp), [VeRyPy](https://github.com/yorak/VeRyPy), or [VRPy](https://github.com/Kuifje02/vrpy).

---

## Contact

- For general inquiries, send email to: info@veroviz.org.
- Follow VeRoViz on Twitter: [@veroviz_org](https://twitter.com/veroviz_org)
- We use a [GitHub issue tracker](https://github.com/optimatorlab/veroviz/issues) to monitor bugs and enhancement requests. Please report any issues you encounter or let us know of any new features you'd like us to incorporate in VeRoViz.


---

## About Us
- [Lan Peng](https://isaac0821.wordpress.com/introduction/) is the VeRoViz Lead Developer.  He is a Ph.D. Student in the Department of Industrial and Systems Engineering at the University at Buffalo.

- [Chase Murray](https://chasemurray.com/) is the VeRoViz Project Director.  He is an Assistant Professor in the Department of Industrial and Systems Engineering at the University at Buffalo.
 
We hope that VeRoViz adds value to your vehicle routing research. As always, we welcome your feedback (in the form of comments about how you're using the tool, issues you're experiencing, or ideas for new functionality).

---

## How to Cite VeRoViz
If you're using VeRoViz in your research, please consider adding a citation. Our manuscript for VeRoViz is currently under review. You may [view this manuscript on SSRN](https://ssrn.com/abstract=3746037). Until this paper appears in a journal, you may cite VeRoViz with the following BibTeX entry:

```
@Misc{veroviz2020,
    title        = {{VeRoViz}: A Vehicle Routing Visualization Toolkit}, 
    author       = {Lan Peng and Chase Murray},
    year         = {2020},
    howpublished = {\url{https://ssrn.com/abstract=3746037}},
    note         = {Accessed: 2021-05-10}
}
```

--- 

## Contribute to VeRoViz

We welcome contributions from the vehicle routing community.  Please, help us make VeRoViz better!

Here's how you can help:
1.  [Report bugs/errors/oddities](https://github.com/optimatorlab/veroviz/issues/new/choose).  This helps us know if something's broken.
2.  [Suggest a new feature](https://github.com/optimatorlab/veroviz/issues/new?assignees=&labels=feature+request&template=feature_request.md&title=).  We tried to think of all of the clever ways people might use VeRoViz, but we probably forgot something.  Let us know what you think would help make your life easier.
3. [Submit a pull request](https://github.com/optimatorlab/veroviz/pulls).  If you have some code that would fix an issue and/or improve VeRoViz, a pull request is the best way to incorporate that code into the package.  We haven't had any pull requests from outside collaborators, so we haven't yet worked out our preferred workflow.  So, if you're thinking of contributing code, please [send us an email](info@veroviz.org) first, so we can jointly decide the best way to collaborate.


---

## Links

- [Project Website](https://veroviz.org) - Includes installation instructions, documentation, and other relevant information.
- [PyPI Website](https://pypi.org/project/veroviz/) - VeRoViz may be installed via `pip`.
- [Change Log](CHANGELOG.md) - A summary of changes associated with each new release of VeRoViz.
- [FAQs](https://veroviz.org/about.html#faqs) - Frequently asked questions.
- [License](LICENSE.md) - VeRoViz is distributed under the MIT license.
- [Credits](CREDITS.md) - This project is made possible by numerous other software packages.
