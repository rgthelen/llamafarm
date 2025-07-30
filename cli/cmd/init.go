package cmd

import (
	"fmt"
	"os"

	"github.com/spf13/cobra"
)

// initCmd represents the init command
var initCmd = &cobra.Command{
	Use:   "init",
	Short: "Initialize a new LlamaFarm project",
	Long:  `Initialize a new LlamaFarm project with a default configuration.`,
	Args:  cobra.MaximumNArgs(1),
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println("Initializing a new LlamaFarm project...")

		// Create a new project directory
		projectDir := "."
		if len(args) > 0 {
			projectDir = args[0]
		}

		if projectDir != "." {
			os.MkdirAll(projectDir, 0755)
		}

		// INSERT_YOUR_CODE
		// Create a default llamafarm.yaml file in the project directory
		configPath := projectDir + "/llamafarm.yaml"
		configContent := []byte("project:\n  name: \"MyLlamaFarmProject\"\n  description: \"A new LlamaFarm project.\"\n")

		if _, err := os.Stat(configPath); err == nil {
			fmt.Printf("llamafarm.yaml already exists at %s\n", configPath)
		} else {
			err := os.WriteFile(configPath, configContent, 0644)
			if err != nil {
				fmt.Printf("Failed to create llamafarm.yaml: %v\n", err)
			} else {
				absPath, err := os.Getwd()
				if err == nil && projectDir != "." {
					absPath = absPath + "/" + projectDir
				}
				fmt.Printf("Created llamafarm.yaml in %s\n", absPath)
			}
		}
	},
}

func init() {
	rootCmd.AddCommand(initCmd)
}
