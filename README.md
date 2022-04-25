# FPV.WTF OPKG Repository
Custom OPKG repository for the FPV.WTF project.

## Usage
Add the following entry to your `opkg.conf`:

```
src/gz fpv.wtf http://placeholder.url
```

Update `opkg` and list packages from repository:

```
opkg update

```

## Adding your package
Fork the repository and add your Github project to `repositories.json`, then submit a PR. Your packages will be automatically added once your PR is merged into master.

Each entry consists of two fields:

```
{
  "repo": "stylesuxx/dji-hd-fpv-dinit",
  "names": [
    "dinit"
  ]
}
```

* **repo**: Github repository name
* **names**: An array of package names. This name is the first part of the actual filename of your ipk package but has also to match the `Package` field in your control file.

Once the deployment runs it will check the latest release of your project, fetch all matching `ipk` files and check the control file:

1. fetch `name_1*.ipk` and `name_2*.ipk`
2. Check if the Package filed matches in each of the ipk's

If everything checks out a new index is build.
Otherwise the build fails and the offending package will be visible in the build logs.
