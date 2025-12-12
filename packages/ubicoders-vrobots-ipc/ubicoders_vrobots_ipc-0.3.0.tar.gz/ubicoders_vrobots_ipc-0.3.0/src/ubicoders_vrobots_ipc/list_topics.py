import time
import argparse
import iceoryx2 as iox2
import zenoh
from colorama import init, Fore, Style

init(autoreset=True)

def matches_keyword(text: str, keyword: str | None, case_sensitive: bool) -> bool:
    if not keyword:
        return True
    return (keyword in text) if case_sensitive else (keyword.lower() in text.lower())

def list_iox2_services(keyword: str | None = None, case_sensitive: bool = False):
    iox2.set_log_level_from_env_or(iox2.LogLevel.Error)
    services = iox2.Service.list(iox2.config.global_config(), iox2.ServiceType.Ipc)

    if not services:
        print("  - No services found")
        return

    # Filter & sort for stable output
    names = [svc.name().to_string() for svc in services]
    filtered = sorted(n for n in names if matches_keyword(n, keyword, case_sensitive))

    if keyword and not filtered:
        print(f"  - No services matched keyword: '{keyword}'")
    else:
        for name in (filtered if keyword else sorted(names)):
            print(f"  - [{Style.BRIGHT}{Fore.MAGENTA}i{Style.RESET_ALL}] {name}")

def list_zenoh_topics(timeout_s: float = 2.0, keyword: str | None = None, case_sensitive: bool = False):
    
    session = zenoh.open(zenoh.Config())
    seen = set()

    def callback(sample):
        key = str(sample.key_expr)
        seen.add(key)

    sub = session.declare_subscriber("**", callback)
    time.sleep(timeout_s)

    filtered = sorted(k for k in seen if matches_keyword(k, keyword, case_sensitive))

    if not seen:
        print("  - No zenoh topics discovered")
    elif keyword and not filtered:
        print(f"  - No zenoh topics matched keyword: '{keyword}'")
    else:
        for key in (filtered if keyword else sorted(seen)):
            print(f"  - [{Style.BRIGHT}{Fore.CYAN}z{Style.RESET_ALL}] {key}")
 
    sub.undeclare()
    session.close()

def main():
    parser = argparse.ArgumentParser(description="Discover zenoh topics and iceoryx2 services.")
    parser.add_argument("-t", "--timeout", type=float, default=0.5, help="Discovery time for zenoh (seconds)")
    parser.add_argument("-k", "--keyword", type=str, default=None, help="Filter topics/services containing this keyword")
    parser.add_argument("--case-sensitive", action="store_true", help="Make keyword matching case-sensitive")
    args = parser.parse_args()

    print(Fore.BLUE + "Listing topics...")
    list_iox2_services(keyword=args.keyword, )
    list_zenoh_topics(timeout_s=args.timeout, keyword=args.keyword, )
    

if __name__ == "__main__":
    main()
