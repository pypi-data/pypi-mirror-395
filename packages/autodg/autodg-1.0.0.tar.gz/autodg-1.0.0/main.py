import argparse
import os
import sys
import warnings
warnings.filterwarnings("ignore", category=SyntaxWarning)
from modules.orchestration.dispatcher import Dispatcher
from modules.orchestration.resolver import Resolver
from modules.output.write_files import MarkdownGenerator

def main():
    parser = argparse.ArgumentParser(description="Python API Analyzer")
    parser.add_argument("--paths", required=True, help="Path to the project root")
    parser.add_argument("--output", default="output", help="Output directory")
    parser.add_argument("--ollama", type=bool, default=False, help="Enable Ollama LLM explanations")
    
    args = parser.parse_args()
    
    project_root = os.path.abspath(args.paths)
    output_dir = os.path.abspath(args.output)
    
    if not os.path.exists(project_root):
        print(f"Error: Project path {project_root} does not exist.")
        sys.exit(1)
        
    print(f"Starting analysis on: {project_root}")
    
    # 1. Dispatcher - Detect and Extract
    dispatcher = Dispatcher(project_root)
    dispatcher.detect_frameworks()
    routes = dispatcher.run()
    
    print(f"Extracted {len(routes)} routes.")
    
    # 2. Resolver - Enrich
    Resolver.resolve(routes, project_root)
    
    # 3. Output - Generate Docs
    if args.ollama and len(routes) > 50:
        print(f"WARNING: You have enabled LLM explanation for {len(routes)} routes.")
        print("This may take a very long time and incur high costs/load.")
        confirm = input("Do you want to continue? (y/n): ")
        if confirm.lower() != 'y':
            print("Aborting LLM generation (generating docs without LLM)...")
            args.ollama = False

    generator = MarkdownGenerator(output_dir, use_llm=args.ollama)
    generator.generate_route_docs(routes)
    generator.generate_file_docs(project_root)
    
    print(f"Analysis complete. Output saved to {output_dir}")

if __name__ == "__main__":
    main()
