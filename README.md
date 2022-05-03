# FPV.WTF OPKG Repository
Custom OPKG repository for the FPV.WTF project.

## Usage
Add the following entry to your `opkg.conf`:

```
src/gz fpv.wtf http://repo.fpv.wtf/pigeon
```

Update `opkg` and list packages from repository:

```
opkg update
```

## Adding your package
Fork the repository and add your Github project to `repositories.json`, then submit a PR. The package index will be rebuilt and your packages will be automatically added once your PR is merged into master.

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

### IPK template
You can check out the [IPK example](https://github.com/stylesuxx/ipk-example) repository. It provides a template in regards to folder structure, a `Makefile` and a workflow to automatically build IPK packages via Github Actions.
