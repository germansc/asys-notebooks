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

        pythonEnv = pkgs.python3.withPackages (ps: with ps; [
          numpy
          matplotlib
          ipython
          ipywidgets
          ipympl
          jupyter
        ]);

        tools = with pkgs; [
            pyright
            ruff
            black
        ];

      in {
        devShells.default = pkgs.mkShell {
          name = "sp-notebooks";
          buildInputs = [ pythonEnv ] ++ tools;
          shellHook = ''
            echo "Jupyter environment ready:"
            jupyter lab
          '';
        };
      }
    );
}
