{
  description = "AI-powered exploratory testing assistant";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            python3
            python3Packages.pip
            python3Packages.virtualenv
            python3Packages.pytest
          ];

          shellHook = ''
            if [ ! -d "venv" ]; then
              python -m virtualenv venv
            fi
            source venv/bin/activate
          '';
        };
      });
} 