package main

import "strings"

// Cleans string from whitespace. Returns cleaned string
func cleanOutput(output string) string {
	output = strings.TrimSpace(output)
	words := strings.Fields(output) // Splits by all whitespace and removes extra spaces
	return strings.Join(words, " ") // Joins words with a single space
}
