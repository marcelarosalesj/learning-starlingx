# StarlingX Build System

## Key concepts:
* Mirror: repository containing all RPM dependencies
* Repo: StarlingX projects/services
* Tools: scripts and tools for StarlingX packages and image building
* Cengn mirror: latest green is [here](http://mirror.starlingx.cengn.ca/mirror/starlingx/master/centos/latest_green_build/)

## StarlingX Build Guide
* [StarlingX Build System 1.0](https://docs.starlingx.io/contributor/build_guides/latest/index.html)
* For every customization it's better to get a successful building environment first, then do the changes and recompile.

## Want to rebuild the image with latest changes?
```
# Update StarlingX Projects (Terminal 2)
cd $MY_REPO_ROOT_DIR
repo sync -j`nproc`

# Update stx-tools (Terminal 3)
cd ~/stx-tools/centos-mirror-tools/
git pull 

# Update mirror (Terminal 1)
cd /localdisk/ 
./download_mirror.sh 
cp -r $HOME/tools/centos-mirror-tools/output/stx-r1/ $HOME/starlingx/mirror/CentOS/

# Clean packages and rebuild image (Terminal 2)
populate_downloads.sh /import/mirrors/CentOS/stx-r1/CentOS/pike/
build-pkgs --clean
generate-cgcs-centos-repo.sh /import/mirrors/CentOS/stx-r1/CentOS/pike/
build-pkgs
build-iso
```

## Want to rebuild one package with own changes?
```
# Do changes on your branch

# Rebuild package
# Note: If you want to build an iso later, do not use --no-build-info flag.
build-pkgs fm-common --clean
build-pkgs fm-common --no-descendants --no-build-info

```
