terraform {
  required_providers {
    external = {
      source  = "hashicorp/external"
      version = ">=2.3.2"
    }
    http = {
      source  = "hashicorp/http"
      version = ">=3.4.0"
    }
    local = {
      source  = "hashicorp/local"
      version = ">=2.4.0"
    }
    time = {
      source  = "hashicorp/time"
      version = ">=0.9.2"
    }
  }
}
