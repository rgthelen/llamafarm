package cmd

import (
	"fmt"

	"github.com/spf13/cobra"
)

// helloCmd represents the hello command
var helloCmd = &cobra.Command{
	Use:   "hello [name]",
	Short: "Greet someone",
	Long: `A simple greeting command that demonstrates how to create
commands with arguments and flags.`,
	Args: cobra.MaximumNArgs(1),
	Run: func(cmd *cobra.Command, args []string) {
		name := "World"
		if len(args) > 0 {
			name = args[0]
		}

		uppercase, _ := cmd.Flags().GetBool("uppercase")
		greeting := fmt.Sprintf("Hello, %s!", name)

		if uppercase {
			greeting = fmt.Sprintf("HELLO, %s!", name)
		}

		fmt.Println(greeting)
	},
}

func init() {
	rootCmd.AddCommand(helloCmd)

	// Add flags to the hello command
	helloCmd.Flags().BoolP("uppercase", "u", false, "Print greeting in uppercase")
}