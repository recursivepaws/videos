{
  description = "Basic flake for working with manim on python";
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
    systems.url = "github:nix-systems/default";
    devenv.url = "github:cachix/devenv";
    flake-utils = {
      url = "github:numtide/flake-utils";
      inputs.systems.follows = "systems";
    };
  };

  outputs = { self, nixpkgs, flake-utils, devenv, ... }@inputs:
    flake-utils.lib.eachDefaultSystem (system:
      let pkgs = nixpkgs.legacyPackages.${system};
      in {
        formatter = pkgs.alejandra;
        packages.devenv-up =
          self.devShells.${system}.default.config.procfileScript;
        devShells.render = devenv.lib.mkShell {
          inherit inputs pkgs;
          modules = [
            ({ pkgs, config, lib, ... }: {
              devenv.root =
                let
                  devenvRootFileContent = builtins.readFile ./devenv.root;
                in
                  lib.mkIf (devenvRootFileContent != "") devenvRootFileContent;
              packages = [ pkgs.gtk4 pkgs.just pkgs.manim ];
            })
          ];
        };
        devShells.default = devenv.lib.mkShell {
          inherit inputs pkgs;
          modules = [
            ({ pkgs, config, lib, ... }: {
              devenv.root =
                let
                  devenvRootFileContent = builtins.readFile ./devenv.root;
                in
                  lib.mkIf (devenvRootFileContent != "") devenvRootFileContent;
              packages = with pkgs; [
                just
                ruff
                manim
                uv
                mpv
                sox

                # Required for manimpango to build
                pkg-config
                cairo
                pango
                gobject-introspection

                # Required for OpenGL/janim
                libGL
                libGLU
                freeglut
                xorg.libX11
                xorg.libXext
                typst

                # Required for PySide6/Qt
                glib
                gst_all_1.gstreamer
                gst_all_1.gst-plugins-base
                libxkbcommon
                fontconfig
                freetype
                dbus
                stdenv.cc.cc.lib
                xorg.libxcb
              ];

              # Set up library paths
              env.LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
                pkgs.libGL
                pkgs.libGLU
                pkgs.freeglut
                pkgs.xorg.libX11
                pkgs.xorg.libXext
                pkgs.typst
                pkgs.glib
                pkgs.gst_all_1.gstreamer
                pkgs.gst_all_1.gst-plugins-base
                pkgs.libxkbcommon
                pkgs.fontconfig
                pkgs.freetype
                pkgs.dbus
                pkgs.stdenv.cc.cc.lib
                pkgs.xorg.libxcb
              ];

              # Qt environment variables
              env.QT_QPA_PLATFORM = "xcb";
              env.QT_PLUGIN_PATH =
                "${pkgs.qt6.qtbase}/${pkgs.qt6.qtbase.qtPluginPrefix}";
            })
          ];
        };
      });

}
