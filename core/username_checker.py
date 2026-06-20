# core/username_checker.py

import aiohttp
import asyncio
import random
import string

class UsernameScanner:
    def __init__(self):
        self.target_sites = {
            # Developer & Tech
            "GitHub": "https://github.com/{}",
            "GitLab": "https://gitlab.com/{}",
            "Replit": "https://replit.com/@{}",
            "HackerRank": "https://www.hackerrank.com/{}",
            "LeetCode": "https://leetcode.com/{}",
            "Dev.to": "https://dev.to/{}",
            "Pastebin": "https://pastebin.com/u/{}",

            # Social, Media & Entertainment
            "Reddit": "https://www.reddit.com/user/{}",
            "Vimeo": "https://vimeo.com/{}",
            "Patreon": "https://www.patreon.com/{}",
            "Spotify": "https://open.spotify.com/user/{}",
            "SoundCloud": "https://soundcloud.com/{}",
            "Pinterest": "https://www.pinterest.com/{}/",

            # Identity & Portfolios
            "Medium": "https://medium.com/@{}",
            "Wattpad": "https://www.wattpad.com/user/{}",
            "Gravatar": "https://en.gravatar.com/{}",
            "About.me": "https://about.me/{}",
            "Linktree": "https://linktr.ee/{}"
        }
        # Dictionary to cache the baseline lengths of fake profiles
        self.baselines = {}
        
    async def _get_baseline(self, session, site_name, url_template, headers):
        """Fetches the response size of an intentionally fake user to detect Soft 404s."""
        if site_name in self.baselines:
            return self.baselines[site_name]
            
        # Generate a random 15-character string that definitely doesn't exist
        fake_user = "xqz_" + "".join(random.choices(string.ascii_lowercase + string.digits, k=11))
        url = url_template.format(fake_user)
        
        try:
            async with session.get(url, headers=headers, timeout=7) as response:
                text = await response.text()
                baseline_length = len(text)
                self.baselines[site_name] = baseline_length
                return baseline_length
        except Exception:
            self.baselines[site_name] = 0
            return 0

    async def _check_site(self, session, site_name, url_template, username):
        """Asynchronously checks a site, using baseline calibration to verify findings."""
        target_url = url_template.format(username)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }
        
        try:
            # 1. Fetch the baseline for this specific site
            baseline_length = await self._get_baseline(session, site_name, url_template, headers)
            
            # 2. Fetch the actual target username
            async with session.get(target_url, headers=headers, timeout=7) as response:
                
                if response.status == 404:
                    return {"site": site_name, "url": target_url, "status": "Not Found"}
                
                elif response.status == 200:
                    text = await response.text()
                    target_length = len(text)
                    html_lower = text.lower()
                    
                    # --- ADVANCED FILTERING LOGIC ---
                    
                    # Filter A: Explicit Login Walls (String Matching)
                    if "log in to continue" in html_lower or "sign in to view" in html_lower:
                        return {"site": site_name, "url": target_url, "status": "Login Wall Redirect"}
                    
                    # Filter B: The Soft 404 (Baseline Calibration)
                    # If the target page size is within 500 bytes of the fake user's page size, it's a generic redirect.
                    if baseline_length > 0 and abs(target_length - baseline_length) < 500:
                        return {"site": site_name, "url": target_url, "status": "Not Found (Soft 404)"}
                    
                    # If it passes both filters, it is highly likely to be a valid profile
                    return {"site": site_name, "url": target_url, "status": "Found"}
                    
                else:
                    return {"site": site_name, "url": target_url, "status": f"Error: {response.status}"}
                    
        except asyncio.TimeoutError:
            return {"site": site_name, "url": target_url, "status": "Timeout"}
        except Exception as e:
            return {"site": site_name, "url": target_url, "status": "Error"}

    async def scan(self, username):
        """Orchestrates the asynchronous scanning of all sites."""
        results = []
        
        async with aiohttp.ClientSession() as session:
            tasks = []
            for site_name, url_template in self.target_sites.items():
                task = asyncio.create_task(
                    self._check_site(session, site_name, url_template, username)
                )
                tasks.append(task)
            
            completed_tasks = await asyncio.gather(*tasks)
            
            for result in completed_tasks:
                if result["status"] == "Found":
                    results.append(result)
                    
        return sorted(results, key=lambda x: x['site'])

# --- Testing the logic independently ---
if __name__ == "__main__":
    async def run_test():
        scanner = UsernameScanner()
        target = "admin"  
        
        print(f"[*] Scanning {len(scanner.target_sites)} platforms with Baseline Calibration...")
        found_accounts = await scanner.scan(target)
        
        if found_accounts:
            print("\n[+] Confirmed Accounts:")
            for account in found_accounts:
                print(f"    - {account['site']}: {account['url']}")
        else:
            print("\n[-] No accounts found.")

    asyncio.run(run_test())
