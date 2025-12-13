use anyhow::Result;
use clap::{Parser, Subcommand};

#[derive(Parser)]
#[command(name = "forks")]
#[command(author, version, about = "forkstack - instant, isolated development environments")]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// Create a new fork
    Create {
        /// Optional name for the fork
        #[arg(short, long)]
        name: Option<String>,
    },
    /// List all forks
    List,
    /// Delete a fork
    Delete {
        /// Name of the fork to delete
        name: String,
    },
}

#[tokio::main]
async fn main() -> Result<()> {
    let cli = Cli::parse();

    match cli.command {
        Commands::Create { name } => {
            let fork = forkstack::create_fork(name).await?;
            println!("Created fork: {}", fork.name);
            println!("Database: {}", fork.database_url);
            println!("Storage:  {}", fork.storage_url);
        }
        Commands::List => {
            let forks = forkstack::list_forks().await?;
            if forks.is_empty() {
                println!("No forks found. Create one with: forks create");
            } else {
                println!("{:<16} {:<12} {}", "NAME", "CREATED", "DATABASE");
                for fork in forks {
                    println!("{:<16} {:<12} {}", fork.name, fork.created_ago(), fork.database_url);
                }
            }
        }
        Commands::Delete { name } => {
            forkstack::delete_fork(&name).await?;
            println!("Deleted fork: {}", name);
        }
    }

    Ok(())
}
