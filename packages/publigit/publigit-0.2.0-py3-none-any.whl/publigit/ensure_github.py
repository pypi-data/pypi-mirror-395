def ensure_github_repo_pygithub(
    repo_name: str,
    private: bool = False,
    token_env: str = "GITHUB_TOKEN",
) -> None:
    """
    Ensure a GitHub repo exists for the current user, and add 'origin' if missing.

    - Uses PyGithub (installed on demand via ensure_pkg).
    - Expects a personal access token in `token_env` (default: GITHUB_TOKEN).
    - If the repo already exists, it is reused.
    - If git remote 'origin' is missing, it will be created (SSH URL).
    """
    token = os.getenv(token_env)
    if not token:
        print(f"\nℹ️  {token_env} not set; skipping GitHub repo creation.")
        return

    # Ensure PyGithub is available
    ensure_pkg("github", "PyGithub")

    from github import Github, GithubException  # type: ignore[import]

    gh = Github(token)

    try:
        user = gh.get_user()
        login = user.login
        full_name = f"{login}/{repo_name}"
        print(f"\nEnsuring GitHub repo exists: {full_name} …")

        try:
            repo = gh.get_repo(full_name)
            print(f"ℹ️  GitHub repo '{full_name}' already exists.")
        except GithubException as e:
            if e.status == 404:
                print(f"Creating GitHub repo '{full_name}' (private={private}) …")
                repo = user.create_repo(
                    repo_name,
                    private=private,
                    auto_init=False,
                    has_issues=True,
                    has_wiki=True,
                )
                print(f"✅ Created GitHub repo: {repo.full_name}")
            else:
                print(f"⚠️  Failed to access GitHub repo '{full_name}': {e}")
                return

        # Ensure local git remote 'origin' is configured
        if not git_remote_exists("origin"):
            ssh_url = repo.ssh_url or repo.clone_url
            print(f"Adding git remote 'origin' -> {ssh_url}")
            try:
                run(["git", "remote", "add", "origin", ssh_url])
            except subprocess.CalledProcessError as e:
                print(f"⚠️  Failed to add 'origin' remote: {e}")
        else:
            print("ℹ️  Git remote 'origin' already exists; not modifying.")

    except Exception as e:  # very defensive to avoid killing the release
        print(f"⚠️  Unexpected error while ensuring GitHub repo: {e}")