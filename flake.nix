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
            python3Packages.ruff
            git
          ];

          shellHook = ''
            if [ ! -d "venv" ]; then
              python -m virtualenv venv
            fi
            source venv/bin/activate
            # Set up a green prompt to indicate nix environment
            export PS1="\[\033[1;32m\][nix-dev]\[\033[0m\] \[\033[1;34m\]\w\[\033[0m\] $ "
          '';
        };
      });
} 