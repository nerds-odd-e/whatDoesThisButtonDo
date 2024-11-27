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

            # Git convenience function
            g() {
              if [ -z "$1" ]; then
                echo "Usage: g <commit message>"
                return 1
              fi
              
              (
                set -e  # Exit on any error
                echo "Running ruff check --fix ."
                ruff check --fix .
                
                echo "Running git add ."
                git add .
                
                echo "Running git commit -m \"$1\""
                git commit -m "$1"
                
                echo "Running git pull --rebase"
                git pull --rebase
                
                echo "Running git push"
                git push
                
                echo "All done! 🎉"
              )
            }

            # Export the function so it's available in subshells
            export -f g
          '';
        };
      });
} 