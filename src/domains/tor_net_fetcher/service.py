import requests
import json
from src.database import get_db
from src.domains.tor_net_fetcher.model import TorVsWebCountryStats
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from src.domains.shared.model import Country
from src.domains.tor_net_fetcher.helper import HUMAN_BASELINES


class TorNetFetchService:
    # Configuration parameters
    avg_request_size_kb = 30.0  # Average HTTP request size in KB
    http_traffic_ratio = 0.7    # 70% of traffic is HTTP/HTTPS
    protocol_overhead_ratio = 0.85  # 85% efficiency after Tor overhead
    
    def process_response_body_for_tor(self, response, country_code):
        """Process relay data and calculate total requests."""
        relays = response.get('relays', [])
        sum_of_request = 0
        country = "None"
        
        print(f"Processing {len(relays)} relays...")
        print("-" * 50)
        
        for relay in relays:
            bandwidth_bps = relay.get('observed_bandwidth', 0)
            avg_request_size_bytes = self.avg_request_size_kb * 1024
            
            effective_bandwidth = bandwidth_bps * self.http_traffic_ratio * self.protocol_overhead_ratio
            requests_per_second = effective_bandwidth / avg_request_size_bytes
            requests_per_day = requests_per_second * 86400
            
            # Get country from first relay (they should all be the same for country-specific query)
            if country == "None":
                country = relay.get('country', 'Unknown')
            
            
            sum_of_request += requests_per_day
        
        print(f"\nTOTAL for {country.upper()}:")
        print(f"Total estimated HTTP requests per day: {sum_of_request:,.0f}")
        
        # Fixed: Return proper dictionary structure
        return {
            "total_requests": sum_of_request,
            "country": country,
            "relay_count": len(relays)
        }
    
    def save_record_to_db(self, db_conn: Session, total_requests: float, country_code: str, tor_traffic: bool):
        """Save statistics to database."""
        try:
            print(f"Saving to database: {total_requests:,.0f} requests for {country_code.upper()}")
            
            # Create record
            record = TorVsWebCountryStats(
                country_code=country_code.upper(),
                tor_traffic=tor_traffic,
                internet_traffic= not(tor_traffic),
                avg_http_request=int(total_requests)  # Convert to integer
            )
            
            # Save to database
            db_conn.merge(record)
            db_conn.commit()
            
            print("✅ Successfully saved to database!")
            return True
            
        except SQLAlchemyError as e:
            print(f"❌ Database error: {e}")
            db_conn.rollback()
            return False
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            db_conn.rollback()
            return False
        

    
    def fetch_live_tor_stats(self, country_code):
        """Fetch live Tor statistics and save to database."""
        try:
            # Build URL for specific country
            url = f"https://onionoo.torproject.org/details?type=relay&search=flag:Exit%20country:{country_code.lower()}&fields=fingerprint,nickname,country,write_history,observed_bandwidth,running,last_seen,consumed_bandwidth&running=true"
            
            print(f"Fetching Tor exit relay data for {country_code.upper()}...")
            
            # Fetch data
            response = requests.get(url)
            response.raise_for_status()  # Raise exception for HTTP errors
            
            data = response.json()
            
            # Process data
            results = self.process_response_body_for_tor(data, country_code)
            is_tor_traffic = True
            # Save to database
            if results["total_requests"] > 0:
                db = next(get_db())
                try:
                    success = self.save_record_to_db(
                        db, 
                        results["total_requests"], 
                        results["country"],
                        is_tor_traffic
                        
                    )
                    
                    if not(success):
                        print("❌ Failed to save to database.")
                        
                finally:
                    db.close()  # Always close the database connection
            else:
                print("⚠️  No relays found or zero requests calculated.")
            
            return results
            
        except requests.RequestException as e:
            print(f"❌ Network error: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing error: {e}")
            return None
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return None


    def get_all_country_codes_from_db(self):
        result = []
        db = next(get_db())
        try:
            all_codes = db.query(Country.code).all()
        finally:
            db.close()
        print(all_codes)
        for country_code, in all_codes:
            result.append(country_code)
        return result
    

    def process_response_body_for_internet(self, data, country_code):
        total_estimated_requests = HUMAN_BASELINES[country_code]
        series = data.get('result', {}).get('serie_0', {})
        values = [float(v) for v in series.get('values')]
        avrg = sum(values)/len(values)
        print(f"avg is {avrg} and total_estimated req is {total_estimated_requests}, total_req per day is {total_estimated_requests* avrg}")
        return {"total_requests" : total_estimated_requests* avrg, "country" : country_code}


    def fetch_live_net_stats(self, country_code):
        """Fetch live Tor statistics and save to database."""
        try:
            # Build URL for specific country
            url = f"https://api.cloudflare.com/client/v4/radar/http/timeseries?aggInterval=1h&dateRange=1d&location={country_code.upper()}&format=json"
            cloudflare_auth_headers = { 'X-Auth-Email': 'shireenbanu89@gmail.com',
                        'X-Auth-Key': '5504c8edcbf9d41817fbae78e9b98fa30216d'
                      }
            
            print(f"Fetching Daily Internet data for {country_code.upper()}...")
            
            # Fetch data
            response = requests.get(url, headers= cloudflare_auth_headers)
            response.raise_for_status()  # Raise exception for HTTP errors
            
            data = response.json()
            print(data)
            
            # Process data
            results = self.process_response_body_for_internet(data, country_code)
            print(f"results[total_requests] =  {results["total_requests"]}")
            is_tor_traffic = False
            # # Save to database
            if  results["total_requests"] > 0:
                db = next(get_db())
                try:
                    success = self.save_record_to_db(
                        db, 
                        results["total_requests"], 
                        results["country"],
                        is_tor_traffic
                    )
                    
                    if not(success):
                        print("❌ Failed to save to database.")
                        
                finally:
                    db.close()  # Always close the database connection
            else:
                print("⚠️  No relays found or zero requests calculated.")
            
            return results
            
        except requests.RequestException as e:
            print(f"❌ Network error: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing error: {e}")
            return None
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return None
        
    def fetch_tor_and_net_stats_for_all_countries(self):
            # Fetch and save German Tor statistics
        country_codes = service.get_all_country_codes_from_db()
        # country_codes = ["US"]
        for country_code in country_codes:
            service.fetch_live_net_stats(country_code)
            service.fetch_live_tor_stats(country_code)
        

if __name__ == "__main__":
    service = TorNetFetchService()
    service.fetch_tor_and_net_stats_for_all_countries()
    

