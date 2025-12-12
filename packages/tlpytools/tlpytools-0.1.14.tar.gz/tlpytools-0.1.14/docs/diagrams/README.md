# 🎼 ORCA Orchestrator Diagrams

This directory contains comprehensive diagrams illustrating the ORCA orchestrator's features, workflows, and architecture.

## 📊 Available Diagrams

### 1. 🌟 Main Features & Components (`orca_main_features.drawio`)
- **Purpose**: High-level overview of ORCA's core features and five main classes
- **Key Elements**:
  - Central orchestrator component
  - Five main classes: OrcaLogger, OrcaDatabank, OrcaFileSync, OrcaState, OrcaOrchestrator
  - Key features: Multi-component integration, operation modes, configurability, data management
  - Supported model components: PopSim, ActivitySim, CVM, Quetzal
  - Data management types: Shared inputs, output archives, configuration files

### 2. 🏠 Local Testing Workflow (`orca_local_workflow.drawio`)
- **Purpose**: Detailed workflow for local development and testing
- **Key Elements**:
  - Two execution options: One-command full run vs. step-by-step control
  - Sequential model execution flow with iteration loops
  - Local data storage structure
  - Benefits of local testing (fast development, easy debugging, cost-effective)

### 3. ☁️ Cloud Production Workflow (`orca_cloud_workflow.drawio`)
- **Purpose**: Comprehensive cloud production workflow with Azure integration
- **Key Elements**:
  - Three phases: Local preparation, cloud execution, monitoring & results
  - Azure Data Lake Storage structure
  - Smart synchronization features (compression, differential sync, conflict resolution)
  - Environment configuration and alternative tools
  - Cloud production benefits

### 4. 📁 File Structure & Flexibility (`orca_file_structure.drawio`)
- **Purpose**: Demonstrates ORCA's flexible architecture for different Python workflows
- **Key Elements**:
  - Complete databank directory structure
  - Configuration flexibility (YAML, environment variables, CLI overrides)
  - Multiple workflow examples (standard, quick testing, assignment-only)
  - Python environment flexibility across different platforms
  - Shared input data management and output archive patterns

### 5. 🔍 Detailed Step Breakdown (`orca_detailed_steps.drawio`)
- **Purpose**: In-depth view of internal processes and sub-steps
- **Key Elements**:
  - Initialize databank detailed steps
  - Run models execution steps
  - Individual model step execution process
  - Cloud synchronization details
  - State management (running, completed, error states)
  - Error recovery and debugging processes
  - Performance monitoring details
  - Output management processes

## 🎯 How to Use These Diagrams

### For New Users
1. Start with **Main Features & Components** to understand what ORCA does
2. Review **Local Testing Workflow** to see how to get started quickly
3. Explore **File Structure & Flexibility** to understand how it works with your models

### For Production Users
1. Study **Cloud Production Workflow** for deployment strategies
2. Reference **Detailed Step Breakdown** for troubleshooting and optimization
3. Use **File Structure & Flexibility** for customizing your model configurations

### For Developers
1. **Main Features & Components** provides the architectural overview
2. **Detailed Step Breakdown** shows internal processes for debugging and enhancement
3. **File Structure & Flexibility** demonstrates extensibility for new model types

## 🛠️ Opening the Diagrams

These diagrams are created in draw.io format and can be opened with:

1. **Online**: Visit [draw.io](https://app.diagrams.net/) and open the `.drawio` files
2. **VS Code**: Install the "Draw.io Integration" extension
3. **Desktop**: Download the draw.io desktop application

## 🎨 Diagram Features

- **Emoji Icons**: Visual elements for quick recognition
- **Color Coding**: Consistent color schemes for different component types
- **Clear Labeling**: Simple, descriptive text for easy understanding
- **Logical Flow**: Arrows and connections showing process flow
- **Hierarchical Organization**: From high-level concepts to detailed implementation

## 📝 Notes for Diagram Updates

When updating these diagrams:
- Maintain consistent color schemes across all diagrams
- Use emojis for visual appeal and quick recognition
- Keep text concise but descriptive
- Ensure all CLI commands and file paths are accurate
- Update version information when features change
