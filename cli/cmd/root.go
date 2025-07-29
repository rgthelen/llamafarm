package cmd

import (
	"fmt"
	"os"

	"github.com/spf13/cobra"
)

var rootCmd = &cobra.Command{
	Use:   "lf",
	Short: "LlamaFarm CLI - Grow AI projects from seed to scale",
	Long: `LlamaFarm CLI is a command line interface for managing and interacting
with your LlamaFarm projects. It provides various commands to help you
manage your data, configurations, models,and operations.`,
	Run: func(cmd *cobra.Command, args []string) {
		// Default behavior when no subcommand is specified
		fmt.Println("Welcome to LlamaFarm!")
		cmd.Help()
	},
}

// Execute adds all child commands to the root command and sets flags appropriately.
// This is called by main.main(). It only needs to happen once to the rootCmd.
func Execute() {
	if err := rootCmd.Execute(); err != nil {
		fmt.Fprintf(os.Stderr, "Error: %v\n", err)
		os.Exit(1)
	}
}

func init() {
	// Here you will define your flags and configuration settings.
	// Cobra supports persistent flags, which, if defined here,
	// will be global for your application.

	// Example of a persistent flag
	// rootCmd.PersistentFlags().StringVar(&cfgFile, "config", "", "config file (default is $HOME/.llamafarm-cli.yaml)")

	// Example of a local flag
	// rootCmd.Flags().BoolP("toggle", "t", false, "Help message for toggle")
}