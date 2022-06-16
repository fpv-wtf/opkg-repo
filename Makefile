OPKG_UTILS_VERSION = opkg-utils-0.5.0
OPKG_UTILS_URL = https://git.yoctoproject.org/opkg-utils/snapshot/$(OPKG_UTILS_VERSION).zip
OPKG_UTILS_PATH = build/$(OPKG_UTILS_VERSION)

all: build pigeon

pigeon:
	@python3 ./fetch-and-validate.py ${TOKEN} --template ./package-list.html --target build/packages/pigeon --html build/packages/pigeon/index.html
	$(OPKG_UTILS_PATH)/opkg-make-index build/packages/pigeon > build/packages/pigeon/Packages
	gzip -c build/packages/pigeon/Packages > build/packages/pigeon/Packages.gz

build:
	mkdir -p build
	mkdir -p build/packages
	mkdir -p build/packages/pigeon
	wget -P build/ $(OPKG_UTILS_URL)
	unzip build/*.zip -d ./build

clean:
	rm -rf ./build

.Phony: all
