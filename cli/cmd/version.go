package cmd

import (
	"fmt"

	"github.com/spf13/cobra"
)

var Version = "1.0.0"

// versionCmd represents the version command
var versionCmd = &cobra.Command{
	Use:   "version",
	Short: "Print the version number of LlamaFarm CLI",
	Long:  "Print the version number of LlamaFarm CLI",
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Printf("LlamaFarm CLI v%s\n", Version)
	},
}

func init() {
	rootCmd.AddCommand(versionCmd)
}