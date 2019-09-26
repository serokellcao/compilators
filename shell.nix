with import <nixpkgs> {};

stdenvNoCC.mkDerivation {
  name = "compilers";
  nativeBuildInputs = [
    nodejs
    chromium

    python2

    pythonPackages.beautifulsoup4
    pythonPackages.requests
    pythonPackages.matplotlib
  ];
  PUPPETEER_SKIP_CHROMIUM_DOWNLOAD = "1";
  PUPPETEER_EXECUTABLE_PATH = "${chromium}/bin/chromium";
}

