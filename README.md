# FPV.WTF OPKG Repository
> Custom OPKG repository for the FPV.WTF project.

This is the official reposiotry from which the [WTFOS configurator](https://github.com/fpv-wtf/wtfos-configurator) pulls its packages.

## Usage
Add the following entry to your `opkg.conf`:

```
src/gz fpv.wtf http://repo.fpv.wtf/pigeon
```

Update `opkg` and list packages from repository:

```
opkg update
```

## Contribute
Your contributions are very welcome, there are a lot of ways to contribute to this project:

* [Add your package to the repo](#adding-your-package)
* [File issues](https://github.com/fpv-wtf/opkg-repo/issues/new) about bugs you find or features you would like to see implemented
* [Submit pull requests](https://github.com/fpv-wtf/opkg-repo/compare) for bugs you have fixed or features you have implemented
* [Join us on Discord](https://discord.com/invite/3rpnBBJKtU) - we have a Discord community and are more than happy to discuss ideas and feedback there

### Submitting a Pull Request
Your bugfixes and improvements are always welcome. If you are unsure about a new feature, feel free to [open an issue](https://github.com/fpv-wtf/opkg-repo/issues/new) for discussion.

When submitting your PR, please submit it against the **develop** branch of this repository.

### Adding your package
Fork the repository and add your Github project to `repositories.json`, then [submit a PR](#submitting-a-pull-request). The package index will be rebuilt and your packages will be automatically added once your PR has been merged into master.

Each entry consists of two fields:

```
{
  "repo": "user/repo-name",
  "names": [
    "name_1",
    "name_2",
  ]
}
```

* **repo**: Github repository name
* **names**: An array of package names. This name is the first part of the actual filename of your ipk package but has also to match the `Package` field in your control file.

> Example: If your package is called `foobar`, then the ipk in your release should be called `foobar_$VERSION_$ARCH.ipk` and the names array should only contain one entry: `foobar`.

Once the deployment runs it will check the latest release of your project, fetch all matching `ipk` files and check the control file:

1. fetch `name_1*.ipk` and `name_2*.ipk`
2. Check if the Package field matches in each of the ipk's

If everything checks out a new index is build.
Otherwise the build fails and the offending package will be visible in the build logs.

### Licensing
Please make sure that the package you are submitting has an open source license attached to it (preferably GPL V3). Pull Requests for packages without a license (or a too restrictive licence) will be rejected.

You can - at any point - run your own repository though (this code is GPL V3) if you are not happy with the licencing term. If you decide to do so make sure that you have some way of supporting your users, since there will be no official support for third party repositories.

### Available architectures
To limit the systems on which your package can be installed, add one of the architectures (from general to specific):

* `pigeon-all`
* `pigeon-glasses` (v1 & v2)
* `pigeon-glasses-v1` or `pigeon-glasses-v2`
* `pigeon-airside` (OG and Lite)
* `pigeon-airside-au` or `pigeon-airside-lite`

### IPK template
You can check out the [IPK example](https://github.com/stylesuxx/ipk-example) repository. It provides a template in regards to folder structure, a `Makefile` and a workflow to automatically build IPK packages via Github Actions.

