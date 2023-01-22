{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-22.11-darwin";
    flake-utils.url = "github:numtide/flake-utils";
  };
  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        projectDir = ./.;
        python = pkgs.python311;
        pythonEnv = pkgs.python311.withPackages (p: [ ]);
      in
      {
        defaultPackage = pythonEnv;
        # nix develop
        devShell = pkgs.mkShell {
          packages = [ pythonEnv pkgs.poetry pkgs.dprint pkgs.libiconv pkgs.darwin.apple_sdk.frameworks.IOKit pkgs.darwin.apple_sdk.frameworks.Security ];
          shellHook = ''
            zsh
          '';
        };
      });
}
