{
  description = "IPS/ASyS | Notebooks Interactivos";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-25.05";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };

        # Raw python packages.
        pythonEnv = pkgs.python3.withPackages (ps: with ps; [
          numpy
          matplotlib
          scipy
          marimo
        ]);

        tools = with pkgs; [
          pyright
          ruff
          uv
        ];

      in {
        devShells.default = pkgs.mkShell {
          name = "asys-notebooks";
          buildInputs = [ pythonEnv ] ++ tools;
          shellHook = ''
            echo "Marimo environment ready."
            echo ""
          '';
        };
      }
    );
}
