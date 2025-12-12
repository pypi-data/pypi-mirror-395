// MCP Server Catalog Schema
// This defines the exact format for catalog.json

// Each server entry must have exactly these fields
#MCPServer: {
	description: string & !=""     // Non-empty description
	command:     string & !=""     // Non-empty command (e.g., "npx", "python", "node")
	args:        [...string]       // Array of string arguments
	env?:        [string]: string  // Optional environment variables (map of string to string)
	repository:  string | null     // Optional repository URL
	categories:  [...string]       // Array of category strings
}

// The catalog is a flat map of server_id -> MCPServer
{
	[string]: #MCPServer
}
