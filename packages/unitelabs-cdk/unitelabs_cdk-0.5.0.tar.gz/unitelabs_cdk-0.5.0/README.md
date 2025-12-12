# UniteLabs Connector Development Framework

The UniteLabs Connector Development Framework (CDK) is a free and open-source framework that enables you to build connectors for
laboratory hard- and software systems with interfaces that are based on industry standards like
[SiLA 2](https://sila-standard.com). If you plan on implementing an interface natively for your device or as wrapper
around an existing proprietary interface, you can use this framework to get it built quickly without deep-diving into
the standard specifications with our intuitive, code-first approach. It provides configurable modules you can use to
quickly integrate the hardware or software you want to connect.

## Installation

[<img src="https://img.shields.io/badge/python-≥3.9.2-0052FF.svg?logo=LOGO&amp;labelColor=090422">](LINK)

The UniteLabs CDK requires Python 3.9 or later. To get started quickly, we recommend to get started with our [cookiecutter starter project](https://gitlab.com/unitelabs/cdk/connector-factory):

```sh
$ cruft create git@gitlab.com:unitelabs/cdk/connector-factory.git
$ cd <my-connector-name>
$ <env-manager> run connector start -vvv
```
where here env-manager would be `poetry`, `hatch`, or `uv`.

You can also manually create a new project from scratch and [install the framework](https://docs.unitelabs.io/connector-development/getting-started/overview) with pip. In this case, of course, you'll be responsible for creating the project boilerplate files yourself.

```sh
$ pip install unitelabs-cdk
```

## Documentation

Explore the UniteLabs [CDK documentation](https://docs.unitelabs.io/connector-development/getting-started/overview) on our docs page. From there you can find your way to the tutorials and guides.

## Contribute

There are many ways to contribute to this project and our vision of freely and readily available interfaces for laboratory systems.

- Check out our [contribution guidelines](https://docs.unitelabs.io/connector-development/community/contributing) to help us improve this project
- Join the over 400 developers in the [SiLA Slack community](https://sila-standard.org/slack)
- Give back to the community and add your connectors to the [UniteHub](https://hub.unitelabs.io) by sending us an
  [email](mailto:connectors@unitelabs.io)!
- Get in touch with our developers regarding feedback and feature requests at [developers@unitelabs.io](mailto:developers@unitelabs.io)
- Give us a ⭐️ on [GitLab](https://gitlab.com/unitelabs/cdk/python-cdk)

## License

We, UniteLabs, provide and maintain this free and open-source framework with the aim to enable the community to overcome
any barriers in digitalizing their laboratory environment. We highly appreciate, if the users of this framework value
the same principles. Therefore, if you want to make your connectors available for others, we encourage you to share them
on our sharing platform, the [UniteHub](https://hub.unitelabs.io). As we do not want to enforce disclosure of your work,
we distribute this framework under the [MIT license](LICENSE).
