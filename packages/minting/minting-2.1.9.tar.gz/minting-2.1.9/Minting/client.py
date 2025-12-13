# import requests
# import pandas as pd
# import io
# import time
# import os
# import sys
# from datetime import datetime
# from pymongo import MongoClient


# # ----------------- Database Layer -----------------
# class Database:
#     def __init__(self, mongo_uri, db_name):
        
#         try:
#             self.client = MongoClient(
#                 mongo_uri,
#                 serverSelectionTimeoutMS=5000,
#                 connectTimeoutMS=10000
#             )
#             # Test connection
#             self.client.server_info()
#             self.db = self.client[db_name]
            
#         except Exception as e:
#             print(f"❌ Connection Error: {e}")
#             raise

#         self.users = self.db["users"]
#         self.access_tokens = self.db["accesstokens"]
#         self.user_plans = self.db["userplans"]
#         self.plans = self.db["plans"]


# # ----------------- Token Manager -----------------
# class TokenManager:
#     def __init__(self, db: Database, raw_token: str):
#         self.db = db
#         self.token = raw_token.strip()

#     def check_token_and_credits(self):
#         """Validate token and check if user has credits"""
#         token_doc = self.db.access_tokens.find_one({
#             "token": self.token,
#             "isActive": True
#         })
        
#         if not token_doc:
#             return {"valid": False, "error": "Invalid or inactive access token"}

#         user_id = token_doc["userId"]

#         plan_doc = self.db.user_plans.find_one({
#             "userId": user_id,
#             "isActive": True,
#             "expiresAt": {"$gte": datetime.utcnow()}
#         })

#         if not plan_doc:
#             return {"valid": False, "error": "No active subscription plan found"}

#         credits = plan_doc.get("creditsRemaining", 0)

#         # If credits <= 0, show warning but allow execution
#         if credits <= 0:
#             print("⚠️  Credits exhausted")

#         return {
#             "valid": True,   # Always allow execution
#             "userId": user_id,
#             "planId": plan_doc["_id"],
#             "creditsRemaining": max(credits, 0)  # Never display negative
#         }

#     def deduct_credit(self):
#         """Deduct one credit (can go negative internally, but display will cap at 0)"""
#         token_doc = self.db.access_tokens.find_one({
#             "token": self.token,
#             "isActive": True
#         })
        
#         if not token_doc:
#             return False

#         user_id = token_doc["userId"]

#         plan_doc = self.db.user_plans.find_one({
#             "userId": user_id,
#             "isActive": True,
#             "expiresAt": {"$gte": datetime.utcnow()}
#         })

#         if not plan_doc:
#             return False

#         # Allow decrement even if credits are 0 (can go negative in DB)
#         result = self.db.user_plans.update_one(
#             {"_id": plan_doc["_id"]},
#             {
#                 "$inc": {"creditsRemaining": -1},
#                 "$set": {"updatedAt": datetime.utcnow()}
#             }
#         )
#         return result.modified_count > 0

#     def get_remaining_credits(self):
#         """Get remaining credits (never negative for display)"""
#         token_doc = self.db.access_tokens.find_one({
#             "token": self.token,
#             "isActive": True
#         })
        
#         if not token_doc:
#             return 0

#         user_id = token_doc["userId"]

#         plan_doc = self.db.user_plans.find_one({
#             "userId": user_id,
#             "isActive": True,
#             "expiresAt": {"$gte": datetime.utcnow()}
#         })

#         if not plan_doc:
#             return 0

#         # Show 0 if negative
#         return max(plan_doc.get("creditsRemaining", 0), 0)

# # ----------------- Client Class -----------------
# class Client:
#     def __init__(
#         self,
#         access_token,
#         base_url="http://34.172.210.29/predict",
#         mongo_uri="mongodb+srv://ankitarrow:ankitarrow@cluster0.zcajdur.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
#         db_name="test"
#     ):
#         self.base_url = base_url
#         self.access_token = access_token.strip()
        
#         print("="*60)
#         print("🚀 Initializing Mintzy")
#         print("="*60)

#         self.db = Database(mongo_uri, db_name)
#         self.token_manager = TokenManager(self.db, self.access_token)

#     def _format_table(self, response_json, tickers, parameters):
#         """Format API response into pandas DataFrame"""
#         try:
#             rows = []
#             result = response_json.get("result", {})

#             for ticker in tickers:
#                 for param in parameters:
#                     if ticker not in result or param not in result[ticker]:
#                         rows.append(pd.DataFrame([{
#                             "Ticker": ticker,
#                             "Parameter": param,
#                             "Error": "No prediction data available"
#                         }]))
#                         continue

#                     raw_data = result[ticker][param].get("data", "")
#                     if not raw_data:
#                         rows.append(pd.DataFrame([{
#                             "Ticker": ticker,
#                             "Parameter": param,
#                             "Error": "Empty prediction data"
#                         }]))
#                         continue

#                     # ✅ Parse CSV data and preserve exact timestamps from JSON
#                     # Split lines and parse manually to preserve timestamp format
#                     lines = raw_data.strip().split('\n')
#                     if len(lines) < 2:
#                         rows.append(pd.DataFrame([{
#                             "Ticker": ticker,
#                             "Parameter": param,
#                             "Error": "Insufficient data"
#                         }]))
#                         continue
                    
#                     # Parse data rows (skip header)
#                     data_rows = []
#                     for line in lines[1:]:  # Skip header line
#                         parts = line.split()
#                         if len(parts) >= 3:
#                             # parts[0] = date, parts[1] = time, parts[2] = predicted value
#                             data_rows.append({
#                                 "Date": parts[0],
#                                 "Time": parts[1],
#                                 "Predicted Price": float(parts[2])
#                             })
                    
#                     if not data_rows:
#                         rows.append(pd.DataFrame([{
#                             "Ticker": ticker,
#                             "Parameter": param,
#                             "Error": "No valid data rows"
#                         }]))
#                         continue
                    
#                     df = pd.DataFrame(data_rows)
                    
#                     pred_col = f"Predicted_{param.capitalize()}"
#                     # Prediction column already created in manual parsing above
                    
#                     df["Ticker"] = ticker
#                     rows.append(df[["Ticker", "Date", "Time", "Predicted Price"]])

#             if rows:
#                 return pd.concat(rows, ignore_index=True)
#             else:
#                 return pd.DataFrame([{"Error": "No data to display"}])

#         except Exception as e:
#             return pd.DataFrame([{"Error": str(e)}])
#     def get_prediction(self, tickers, time_frame, parameters):
#             """
#             Get stock predictions (single run only, no auto-refresh).
            
#             Args:
#                 tickers: String or list of stock tickers (max 3)
#                 time_frame: Time frame for predictions (e.g., "4 hours", "1 day")
#                 parameters: String or list of parameters to predict (e.g., ["close", "open"])
            
#             Returns:
#                 dict: Response with success status and data/error
#             """
#             # Normalize tickers
#             if isinstance(tickers, str):
#                 tickers = [tickers]
#             if not isinstance(tickers, list):
#                 return {"success": False, "error": "Tickers must be a string or list"}
#             if len(tickers) > 3:
#                 return {"success": False, "error": "Maximum of 3 tickers allowed"}

#             # Normalize parameters
#             if isinstance(parameters, str):
#                 parameters = [parameters]

#             try:
#                 print("\n" + "="*60)
#                 print("📊 Getting Predictions")
#                 print("="*60)
                
#                 # Check token and credits
#                 token_check = self.token_manager.check_token_and_credits()
#                 if not token_check["valid"]:
#                     print(f"❌ {token_check['error']}")
#                     return {"success": False, "error": token_check["error"]}

#                 print(f"Tickers: {', '.join(tickers)}")
#                 print(f" Time Frame: {time_frame}")
#                 print(f"Parameters: {', '.join(parameters)}")

#                 # Prepare payload
#                 payload = {
#                     "action": {
#                         "action_type": "predict",
#                         "predict": {
#                             "given": {
#                                 "ticker": tickers,
#                                 "time_frame": time_frame
#                             },
#                             "required": {
#                                 "parameters": parameters
#                             }
#                         }
#                     }
#                 }

#                 # Send request
#                 print("\n⏳ Fetching Predictions ...")
#                 response = requests.post(
#                     self.base_url,
#                     json=payload,
#                     headers={"X-Access-Token": self.access_token},
#                     timeout=30
#                 )
#                 response.raise_for_status()
#                 response_json = response.json()
                
                

#                 # Format results
#                 df = self._format_table(response_json, tickers, parameters)

#                 # Deduct credit
#                 if self.token_manager.deduct_credit():
#                     remaining = self.token_manager.get_remaining_credits()
#                 else:
#                     remaining = token_check["creditsRemaining"] - 1

#                 # Display results
#                 print("\n" + "="*60)
#                 print(f"📊 Predictions ({time_frame})")
#                 print("="*60)
#                 print(df.to_string(index=False))
#                 print("="*60)
#                 print(f"💳 Remaining credits: {remaining}")
#                 print("="*60)

#                 return {
#                     "success": True,
#                     "data": df,
#                     "credits_remaining": remaining,
#                     "timestamp": datetime.now().isoformat()
#                 }

#             except requests.exceptions.Timeout:
#                 error_msg = "Request timed out. Please try again."
#                 print(f"❌ {error_msg}")
#                 return {"success": False, "error": error_msg}

#             except requests.exceptions.RequestException as e:
#                 error_msg = f"API request failed: {str(e)}"
#                 print(f"❌ {error_msg}")
#                 return {"success": False, "error": error_msg}

#             except Exception as e:
#                 error_msg = f"Unexpected error: {str(e)}"
#                 print(f"❌ {error_msg}")
#                 return {"success": False, "error": error_msg}

#     def get_credits(self):
#             """Get remaining credits for the current token"""
#             credits = self.token_manager.get_remaining_credits()
#             print(f"💳 Remaining credits: {credits}")
#             return credits


# import requests
# import pandas as pd
# import io
# import time
# import os
# import sys
# import hashlib
# from datetime import datetime
# from pymongo import MongoClient


# # ----------------- Database Layer -----------------
# class Database:
#     def __init__(self, mongo_uri, db_name):
        
#         try:
#             self.client = MongoClient(
#                 mongo_uri,
#                 serverSelectionTimeoutMS=5000,
#                 connectTimeoutMS=10000
#             )
#             # Test connection
#             self.client.server_info()
#             self.db = self.client[db_name]
            
#         except Exception as e:
#             print(f"❌ Connection Error: {e}")
#             raise

#         self.users = self.db["users"]
#         self.access_tokens = self.db["accesstokens"]
#         self.user_plans = self.db["userplans"]
#         self.plans = self.db["plans"]


# # ----------------- Token Manager -----------------
# class TokenManager:
#     def __init__(self, db: Database, raw_token: str):
#         self.db = db
#         self.raw_token = raw_token.strip()
#         self.hashed_token = self._hash_token(self.raw_token)

#     def _hash_token(self, token: str) -> str:
#         """Hash token using SHA-256 (equivalent to Node.js crypto.createHash)"""
#         return hashlib.sha256(token.encode('utf-8')).hexdigest()

#     def check_token_and_credits(self):
#         """Validate token and check if user has credits"""
#         token_doc = self.db.access_tokens.find_one({
#             "token": self.hashed_token,
#             "isActive": True
#         })
        
#         if not token_doc:
#             return {"valid": False, "error": "Invalid or inactive access token"}

#         user_id = token_doc["userId"]

#         plan_doc = self.db.user_plans.find_one({
#             "userId": user_id,
#             "isActive": True,
#             "expiresAt": {"$gte": datetime.utcnow()}
#         })

#         if not plan_doc:
#             return {"valid": False, "error": "No active subscription plan found"}

#         credits = plan_doc.get("creditsRemaining", 0)

#         # If credits <= 0, show warning but allow execution
#         if credits <= 0:
#             print("⚠️  Credits exhausted")

#         return {
#             "valid": True,   # Always allow execution
#             "userId": user_id,
#             "planId": plan_doc["_id"],
#             "creditsRemaining": max(credits, 0)  # Never display negative
#         }

#     def deduct_credit(self):
#         """Deduct one credit (can go negative internally, but display will cap at 0)"""
#         token_doc = self.db.access_tokens.find_one({
#             "token": self.hashed_token,
#             "isActive": True
#         })
        
#         if not token_doc:
#             return False

#         user_id = token_doc["userId"]

#         plan_doc = self.db.user_plans.find_one({
#             "userId": user_id,
#             "isActive": True,
#             "expiresAt": {"$gte": datetime.utcnow()}
#         })

#         if not plan_doc:
#             return False

#         # Allow decrement even if credits are 0 (can go negative in DB)
#         result = self.db.user_plans.update_one(
#             {"_id": plan_doc["_id"]},
#             {
#                 "$inc": {"creditsRemaining": -1},
#                 "$set": {"updatedAt": datetime.utcnow()}
#             }
#         )
#         return result.modified_count > 0

#     def get_remaining_credits(self):
#         """Get remaining credits (never negative for display)"""
#         token_doc = self.db.access_tokens.find_one({
#             "token": self.hashed_token,
#             "isActive": True
#         })
        
#         if not token_doc:
#             return 0

#         user_id = token_doc["userId"]

#         plan_doc = self.db.user_plans.find_one({
#             "userId": user_id,
#             "isActive": True,
#             "expiresAt": {"$gte": datetime.utcnow()}
#         })

#         if not plan_doc:
#             return 0

#         # Show 0 if negative
#         return max(plan_doc.get("creditsRemaining", 0), 0)

# # ----------------- Client Class -----------------
# class Client:
#     # Supported tickers - only these are allowed
#     SUPPORTED_TICKERS = {
#         "RELIANCE", "BHARTIARTL", "TCS", "ICICIBANK", "SBIN", 
#         "INFY", "HINDUNILVR", "HDFCLIFE", "BAJFINANCE", "ITC", 
#         "LT", "MARUTI", "HCLTECH", "KOTAKBANK", "SUNPHARMA", 
#         "ULTRACEMCO", "AXISBANK", "NTPC", "BAJAJFINSV"
#     }
    
#     def __init__(
#         self,
#         access_token,
#         base_url="http://34.172.210.29/predict",
#         mongo_uri="mongodb+srv://ankitarrow:ankitarrow@cluster0.zcajdur.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
#         db_name="test"
#     ):
#         self.base_url = base_url
#         self.access_token = access_token.strip()
        
#         print("="*60)
#         print(" Initializing Mintzy")
#         print("="*60)

#         self.db = Database(mongo_uri, db_name)
#         self.token_manager = TokenManager(self.db, self.access_token)

#     def _format_table(self, response_json, tickers, parameters):
#         """Format API response into pandas DataFrame"""
#         try:
#             rows = []
#             result = response_json.get("result", {})

#             for ticker in tickers:
#                 for param in parameters:
#                     if ticker not in result or param not in result[ticker]:
#                         rows.append(pd.DataFrame([{
#                             "Ticker": ticker,
#                             "Parameter": param,
#                             "Error": "No prediction data available"
#                         }]))
#                         continue

#                     raw_data = result[ticker][param].get("data", "")
#                     if not raw_data:
#                         rows.append(pd.DataFrame([{
#                             "Ticker": ticker,
#                             "Parameter": param,
#                             "Error": "Empty prediction data"
#                         }]))
#                         continue

#                     # ✅ Parse CSV data and preserve exact timestamps from JSON
#                     # Split lines and parse manually to preserve timestamp format
#                     lines = raw_data.strip().split('\n')
#                     if len(lines) < 2:
#                         rows.append(pd.DataFrame([{
#                             "Ticker": ticker,
#                             "Parameter": param,
#                             "Error": "Insufficient data"
#                         }]))
#                         continue
                    
#                     # Parse data rows (skip header)
#                     data_rows = []
#                     for line in lines[1:]:  # Skip header line
#                         parts = line.split()
#                         if len(parts) >= 3:
#                             # parts[0] = date, parts[1] = time, parts[2] = predicted value
#                             data_rows.append({
#                                 "Date": parts[0],
#                                 "Time": parts[1],
#                                 "Predicted Price": float(parts[2])
#                             })
                    
#                     if not data_rows:
#                         rows.append(pd.DataFrame([{
#                             "Ticker": ticker,
#                             "Parameter": param,
#                             "Error": "No valid data rows"
#                         }]))
#                         continue
                    
#                     df = pd.DataFrame(data_rows)
                    
#                     pred_col = f"Predicted_{param.capitalize()}"
#                     # Prediction column already created in manual parsing above
                    
#                     df["Ticker"] = ticker
#                     rows.append(df[["Ticker", "Date", "Time", "Predicted Price"]])

#             if rows:
#                 return pd.concat(rows, ignore_index=True)
#             else:
#                 return pd.DataFrame([{"Error": "No data to display"}])

#         except Exception as e:
#             return pd.DataFrame([{"Error": str(e)}])
    
#     def get_prediction(self, tickers, time_frame, parameters):
#         """
#         Get stock predictions (single run only, no auto-refresh).
        
#         Args:
#             tickers: String or list of stock tickers (max 3)
#             time_frame: Time frame for predictions (e.g., "4 hours", "1 day")
#             parameters: String or list of parameters to predict (e.g., ["close", "open"])
        
#         Returns:
#             dict: Response with success status and data/error
#         """
#         # Normalize tickers
#         if isinstance(tickers, str):
#             tickers = [tickers]
#         if not isinstance(tickers, list):
#             return {"success": False, "error": "Tickers must be a string or list"}
#         if len(tickers) > 3:
#             return {"success": False, "error": "Maximum of 3 tickers allowed"}
        
#         # Validate tickers against supported list
#         invalid_tickers = [t for t in tickers if t.upper() not in self.SUPPORTED_TICKERS]
#         if invalid_tickers:
#             error_msg = f"Ticker(s) not supported currently: {', '.join(invalid_tickers)}"
#             print(f" {error_msg}")
#             print(f"\n Supported tickers: {', '.join(sorted(self.SUPPORTED_TICKERS))}")
#             return {"success": False, "error": error_msg}
        
#         # Normalize ticker case to uppercase
#         tickers = [t.upper() for t in tickers]

#         # Normalize parameters
#         if isinstance(parameters, str):
#             parameters = [parameters]

#         try:
#             print("\n" + "="*60)
#             print("Getting Predictions")
#             print("="*60)
            
#             # Check token and credits
#             token_check = self.token_manager.check_token_and_credits()
#             if not token_check["valid"]:
#                 print(f" {token_check['error']}")
#                 return {"success": False, "error": token_check["error"]}

#             print(f"Tickers: {', '.join(tickers)}")
#             print(f" Time Frame: {time_frame}")
#             print(f"Parameters: {', '.join(parameters)}")

#             # Prepare payload
#             payload = {
#                 "action": {
#                     "action_type": "predict",
#                     "predict": {
#                         "given": {
#                             "ticker": tickers,
#                             "time_frame": time_frame
#                         },
#                         "required": {
#                             "parameters": parameters
#                         }
#                     }
#                 }
#             }

#             # Send request
#             print("\n Fetching Predictions ...")
#             response = requests.post(
#                 self.base_url,
#                 json=payload,
#                 headers={"X-Access-Token": self.access_token},
#                 timeout=30
#             )
#             response.raise_for_status()
#             response_json = response.json()
            
            

#             # Format results
#             df = self._format_table(response_json, tickers, parameters)

#             # Deduct credit
#             if self.token_manager.deduct_credit():
#                 remaining = self.token_manager.get_remaining_credits()
#             else:
#                 remaining = token_check["creditsRemaining"] - 1

#             # Display results
#             print("\n" + "="*60)
#             print(f" Predictions ({time_frame})")
#             print("="*60)
#             print(df.to_string(index=False))
#             print("="*60)
#             print(f" Remaining credits: {remaining}")
#             print("="*60)

#             return {
#                 "success": True,
#                 "data": df,
#                 "credits_remaining": remaining,
#                 "timestamp": datetime.now().isoformat()
#             }

#         except requests.exceptions.Timeout:
#             error_msg = "Request timed out. Please try again."
#             print(f" {error_msg}")
#             return {"success": False, "error": error_msg}

#         except requests.exceptions.RequestException as e:
#             error_msg = f"API request failed: {str(e)}"
#             print(f" {error_msg}")
#             return {"success": False, "error": error_msg}

#         except Exception as e:
#             error_msg = f"Unexpected error: {str(e)}"
#             print(f" {error_msg}")
#             return {"success": False, "error": error_msg}

#     def get_credits(self):
#         """Get remaining credits for the current token"""
#         credits = self.token_manager.get_remaining_credits()
#         print(f" Remaining credits: {credits}")
#         return credits


# import requests
# import pandas as pd
# import io
# import time
# import os
# import sys
# import hashlib
# from datetime import datetime
# from pymongo import MongoClient


# # ----------------- Database Layer -----------------
# class Database:
#     def __init__(self, mongo_uri, db_name):
        
#         try:
#             self.client = MongoClient(
#                 mongo_uri,
#                 serverSelectionTimeoutMS=5000,
#                 connectTimeoutMS=10000
#             )
#             # Test connection
#             self.client.server_info()
#             self.db = self.client[db_name]
            
#         except Exception as e:
#             print(f"❌ Connection Error: {e}")
#             raise

#         self.users = self.db["users"]
#         self.access_tokens = self.db["accesstokens"]
#         self.user_plans = self.db["userplans"]
#         self.plans = self.db["plans"]


# # ----------------- Token Manager -----------------
# class TokenManager:
#     def __init__(self, db: Database, raw_token: str):
#         self.db = db
#         self.raw_token = raw_token.strip()
#         self.hashed_token = self._hash_token(self.raw_token)

#     def _hash_token(self, token: str) -> str:
#         """Hash token using SHA-256 (equivalent to Node.js crypto.createHash)"""
#         return hashlib.sha256(token.encode('utf-8')).hexdigest()

#     def check_token_and_credits(self):
#         """Validate token and check if user has credits"""
#         token_doc = self.db.access_tokens.find_one({
#             "token": self.hashed_token,
#             "isActive": True
#         })
        
#         if not token_doc:
#             return {"valid": False, "error": "Invalid or inactive access token"}

#         user_id = token_doc["userId"]

#         plan_doc = self.db.user_plans.find_one({
#             "userId": user_id,
#             "isActive": True,
#             "expiresAt": {"$gte": datetime.utcnow()}
#         })

#         if not plan_doc:
#             return {"valid": False, "error": "No active subscription plan found"}

#         credits = plan_doc.get("creditsRemaining", 0)

#         # ✅ CHANGED: Block execution if credits <= 0
#         if credits <= 0:
#             return {
#                 "valid": False, 
#                 "error": "Credits exhausted. Please subscribe to a plan to continue.",
#                 "creditsRemaining": 0
#             }

#         return {
#             "valid": True,
#             "userId": user_id,
#             "planId": plan_doc["_id"],
#             "creditsRemaining": credits
#         }

#     def deduct_credit(self):
#         """Deduct one credit (only if credits > 0)"""
#         token_doc = self.db.access_tokens.find_one({
#             "token": self.hashed_token,
#             "isActive": True
#         })
        
#         if not token_doc:
#             return False

#         user_id = token_doc["userId"]

#         plan_doc = self.db.user_plans.find_one({
#             "userId": user_id,
#             "isActive": True,
#             "expiresAt": {"$gte": datetime.utcnow()}
#         })

#         if not plan_doc:
#             return False

#         # ✅ CHANGED: Only deduct if credits > 0
#         current_credits = plan_doc.get("creditsRemaining", 0)
#         if current_credits <= 0:
#             return False

#         result = self.db.user_plans.update_one(
#             {"_id": plan_doc["_id"], "creditsRemaining": {"$gt": 0}},
#             {
#                 "$inc": {"creditsRemaining": -1},
#                 "$set": {"updatedAt": datetime.utcnow()}
#             }
#         )
#         return result.modified_count > 0

#     def get_remaining_credits(self):
#         """Get remaining credits"""
#         token_doc = self.db.access_tokens.find_one({
#             "token": self.hashed_token,
#             "isActive": True
#         })
        
#         if not token_doc:
#             return 0

#         user_id = token_doc["userId"]

#         plan_doc = self.db.user_plans.find_one({
#             "userId": user_id,
#             "isActive": True,
#             "expiresAt": {"$gte": datetime.utcnow()}
#         })

#         if not plan_doc:
#             return 0

#         return max(plan_doc.get("creditsRemaining", 0), 0)

# # ----------------- Client Class -----------------
# class Client:
#     # Supported tickers - only these are allowed
#     SUPPORTED_TICKERS = {
#         "RELIANCE", "BHARTIARTL", "TCS", "ICICIBANK", "SBIN", 
#         "INFY", "HINDUNILVR", "HDFCLIFE", "BAJFINANCE", "ITC", 
#         "LT", "MARUTI", "HCLTECH", "KOTAKBANK", "SUNPHARMA", 
#         "ULTRACEMCO", "AXISBANK", "NTPC", "BAJAJFINSV"
#     }
    
#     def __init__(
#         self,
#         access_token,
#         base_url="http://34.172.210.29/predict",
#         mongo_uri="mongodb+srv://ankitarrow:ankitarrow@cluster0.zcajdur.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
#         db_name="test"
#     ):
#         self.base_url = base_url
#         self.access_token = access_token.strip()
        
#         print("="*60)
#         print(" Initializing Mintzy")
#         print("="*60)

#         self.db = Database(mongo_uri, db_name)
#         self.token_manager = TokenManager(self.db, self.access_token)

#     def _format_table(self, response_json, tickers, parameters):
#         """Format API response into pandas DataFrame"""
#         try:
#             rows = []
#             result = response_json.get("result", {})

#             for ticker in tickers:
#                 for param in parameters:
#                     if ticker not in result or param not in result[ticker]:
#                         rows.append(pd.DataFrame([{
#                             "Ticker": ticker,
#                             "Parameter": param,
#                             "Error": "No prediction data available"
#                         }]))
#                         continue

#                     raw_data = result[ticker][param].get("data", "")
#                     if not raw_data:
#                         rows.append(pd.DataFrame([{
#                             "Ticker": ticker,
#                             "Parameter": param,
#                             "Error": "Empty prediction data"
#                         }]))
#                         continue

#                     # Parse CSV data and preserve exact timestamps from JSON
#                     lines = raw_data.strip().split('\n')
#                     if len(lines) < 2:
#                         rows.append(pd.DataFrame([{
#                             "Ticker": ticker,
#                             "Parameter": param,
#                             "Error": "Insufficient data"
#                         }]))
#                         continue
                    
#                     # Parse data rows (skip header)
#                     data_rows = []
#                     for line in lines[1:]:  # Skip header line
#                         parts = line.split()
#                         if len(parts) >= 3:
#                             data_rows.append({
#                                 "Date": parts[0],
#                                 "Time": parts[1],
#                                 "Predicted Price": float(parts[2])
#                             })
                    
#                     if not data_rows:
#                         rows.append(pd.DataFrame([{
#                             "Ticker": ticker,
#                             "Parameter": param,
#                             "Error": "No valid data rows"
#                         }]))
#                         continue
                    
#                     df = pd.DataFrame(data_rows)
#                     df["Ticker"] = ticker
#                     rows.append(df[["Ticker", "Date", "Time", "Predicted Price"]])

#             if rows:
#                 return pd.concat(rows, ignore_index=True)
#             else:
#                 return pd.DataFrame([{"Error": "No data to display"}])

#         except Exception as e:
#             return pd.DataFrame([{"Error": str(e)}])
    
#     def get_prediction(self, tickers, time_frame, parameters):
     
#         # Normalize tickers
#         if isinstance(tickers, str):
#             tickers = [tickers]
#         if not isinstance(tickers, list):
#             return {"success": False, "error": "Tickers must be a string or list"}
#         if len(tickers) > 3:
#             return {"success": False, "error": "Maximum of 3 tickers allowed"}
        
#         # Validate tickers against supported list
#         invalid_tickers = [t for t in tickers if t.upper() not in self.SUPPORTED_TICKERS]
#         if invalid_tickers:
#             error_msg = f"Ticker(s) not supported currently: {', '.join(invalid_tickers)}"
#             print(f"❌ {error_msg}")
#             print(f"\n✅ Supported tickers: {', '.join(sorted(self.SUPPORTED_TICKERS))}")
#             return {"success": False, "error": error_msg}
        
#         # Normalize ticker case to uppercase
#         tickers = [t.upper() for t in tickers]

#         # Normalize parameters
#         if isinstance(parameters, str):
#             parameters = [parameters]

#         try:
#             print("\n" + "="*60)
#             print("Getting Predictions")
#             print("="*60)
            
#             # ✅ CHANGED: Check token and credits - will now fail if credits <= 0
#             token_check = self.token_manager.check_token_and_credits()
#             if not token_check["valid"]:
#                 print(f"❌ {token_check['error']}")
#                 return {"success": False, "error": token_check["error"]}

#             print(f"📊 Tickers: {', '.join(tickers)}")
#             print(f"⏰ Time Frame: {time_frame}")
#             print(f"📈 Parameters: {', '.join(parameters)}")

#             # Prepare payload
#             payload = {
#                 "action": {
#                     "action_type": "predict",
#                     "predict": {
#                         "given": {
#                             "ticker": tickers,
#                             "time_frame": time_frame
#                         },
#                         "required": {
#                             "parameters": parameters
#                         }
#                     }
#                 }
#             }

#             # Send request
#             print("\n🔄 Fetching Predictions ...")
#             response = requests.post(
#                 self.base_url,
#                 json=payload,
#                 headers={"X-Access-Token": self.access_token},
#                 timeout=30
#             )
#             response.raise_for_status()
#             response_json = response.json()

#             # Format results
#             df = self._format_table(response_json, tickers, parameters)

#             # ✅ CHANGED: Deduct credit and get updated remaining count
#             if self.token_manager.deduct_credit():
#                 remaining = self.token_manager.get_remaining_credits()
#             else:
#                 remaining = 0

#             # Display results
#             print("\n" + "="*60)
#             print(f"✅ Predictions ({time_frame})")
#             print("="*60)
#             print(df.to_string(index=False))
#             print("="*60)
#             print(f"💳 Remaining credits: {remaining}")
            
#             # ✅ CHANGED: Warn if credits are getting low
#             if remaining <= 10:
#                 print(f"⚠️  Warning: Only {remaining} credits remaining!")
#             if remaining == 0:
#                 print("❌ Credits exhausted! Please subscribe to a plan to continue.")
            
#             print("="*60)

#             return {
#                 "success": True,
#                 "data": df,
#                 "credits_remaining": remaining,
#                 "timestamp": datetime.now().isoformat()
#             }

#         except requests.exceptions.Timeout:
#             error_msg = "Request timed out. Please try again."
#             print(f"❌ {error_msg}")
#             return {"success": False, "error": error_msg}

#         except requests.exceptions.RequestException as e:
#             error_msg = f"API request failed: {str(e)}"
#             print(f"❌ {error_msg}")
#             return {"success": False, "error": error_msg}

#         except Exception as e:
#             error_msg = f"Unexpected error: {str(e)}"
#             print(f"❌ {error_msg}")
#             return {"success": False, "error": error_msg}

#     def get_credits(self):
#         """Get remaining credits for the current token"""
#         credits = self.token_manager.get_remaining_credits()
#         print(f"💳 Remaining credits: {credits}")
#         return credits

# updated code for client 
import requests
import pandas as pd
import io
import time
import os
import sys
import hashlib
from datetime import datetime
from pymongo import MongoClient


# ----------------- Database Layer -----------------
class Database:
    def __init__(self, mongo_uri, db_name):
        
        try:
            self.client = MongoClient(
                mongo_uri,
                serverSelectionTimeoutMS=50000,
                connectTimeoutMS=100000
            )
            # Test connection
            self.client.server_info()
            self.db = self.client[db_name]
            
        except Exception as e:
            print(f"❌ Connection Error: {e}")
            raise

        self.users = self.db["users"]
        self.access_tokens = self.db["accesstokens"]
        self.user_plans = self.db["userplans"]
        self.plans = self.db["plans"]


# ----------------- Token Manager -----------------
class TokenManager:
    def __init__(self, db: Database, raw_token: str):
        self.db = db
        self.raw_token = raw_token.strip()
        self.hashed_token = self._hash_token(self.raw_token)

    def _hash_token(self, token: str) -> str:
        """Hash token using SHA-256 (equivalent to Node.js crypto.createHash)"""
        return hashlib.sha256(token.encode('utf-8')).hexdigest()

    def check_token_and_credits(self):
        """Validate token and check if user has credits"""
        token_doc = self.db.access_tokens.find_one({
            "token": self.hashed_token,
            "isActive": True
        })
        
        if not token_doc:
            return {"valid": False, "error": "Invalid or inactive access token"}

        user_id = token_doc["userId"]

        plan_doc = self.db.user_plans.find_one({
            "userId": user_id,
            "isActive": True,
            "expiresAt": {"$gte": datetime.utcnow()}
        })

        if not plan_doc:
            return {"valid": False, "error": "No active subscription plan found"}

        credits = plan_doc.get("creditsRemaining", 0)

        if credits <= 0:
            return {
                "valid": False, 
                "error": "Credits exhausted. Please subscribe to a plan to continue.",
                "creditsRemaining": 0
            }

        return {
            "valid": True,
            "userId": user_id,
            "planId": plan_doc["_id"],
            "creditsRemaining": credits
        }

    def deduct_credit(self):
        """Deduct one credit (only if credits > 0)"""
        token_doc = self.db.access_tokens.find_one({
            "token": self.hashed_token,
            "isActive": True
        })
        
        if not token_doc:
            return False

        user_id = token_doc["userId"]

        plan_doc = self.db.user_plans.find_one({
            "userId": user_id,
            "isActive": True,
            "expiresAt": {"$gte": datetime.utcnow()}
        })

        if not plan_doc:
            return False

        current_credits = plan_doc.get("creditsRemaining", 0)
        if current_credits <= 0:
            return False

        result = self.db.user_plans.update_one(
            {"_id": plan_doc["_id"], "creditsRemaining": {"$gt": 0}},
            {
                "$inc": {"creditsRemaining": -1},
                "$set": {"updatedAt": datetime.utcnow()}
            }
        )
        return result.modified_count > 0

    def get_remaining_credits(self):
        """Get remaining credits"""
        token_doc = self.db.access_tokens.find_one({
            "token": self.hashed_token,
            "isActive": True
        })
        
        if not token_doc:
            return 0

        user_id = token_doc["userId"]

        plan_doc = self.db.user_plans.find_one({
            "userId": user_id,
            "isActive": True,
            "expiresAt": {"$gte": datetime.utcnow()}
        })

        if not plan_doc:
            return 0

        return max(plan_doc.get("creditsRemaining", 0), 0)

# ----------------- Client Class -----------------
class Client:
    # Supported tickers - only these are allowed
    SUPPORTED_TICKERS = {
    "TCS",
    "HDFCBANK",
    "BHARTIARTL",
    "ICICIBANK",
    "SBIN",
    "INFY",
    "BAJFINANCE",
    "HINDUNILVR",
    "ITC",
    "MARUTI",
    "HCLTECH",
    "SUNPHARMA",
    "KOTAKBANK",
    "AXISBANK",
    "TATAMOTORS",
    "ULTRACEMCO",
    "BAJAJFINSV",
    "ADANIPORTS",
    "NTPC",
    "ONGC",
    "ASIANPAINT",
    "JSWSTEEL",
    "ADANIPOWER",
    "WIPRO",
    "ADANIENT",
    "POWERGRID",
    "NESTLEIND",
    "COALINDIA",
    "INDIGO",
    "HINDZINC",
    "TATASTEEL",
    "VEDL",
    "SBILIFE",
    "EICHERMOT",
    "GRASIM",
    "HINDALCO",
    "LTIM",
    "TVSMOTOR",
    "DIVISLAB",
    "HDFCLIFE",
    "PIDILITIND",
    "CHOLAFIN",
    "BRITANNIA",
    "AMBUJACEM",
    "GAIL",
    "BANKBARODA",
    "GODREJCP",
    "HEROMOTOCO",
    "TATAPOWER",

    }
    
    def __init__(
        self,
        access_token=None,   # new kw
        token=None,          # old kw / positional
        base_url="http://35.184.240.180/predict",
        mongo_uri="mongodb+srv://ankitarrow:ankitarrow@cluster0.zcajdur.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
        db_name="test"
    ):
        # allow: Client(access_token="..."), Client(token="..."), Client("...")
        if access_token is None and token is None:
            raise ValueError("Access token must be provided as 'access_token' or 'token'.")

        # if called positionally, first arg will land in access_token
        self.access_token = (access_token or token).strip()
        self.base_url = base_url
        
        print("="*60)
        print(" Initializing Mintzy")
        print("="*60)

        self.db = Database(mongo_uri, db_name)
        self.token_manager = TokenManager(self.db, self.access_token)

    def _format_table(self, response_json, tickers, parameters):
        """Format API response into pandas DataFrame"""
        try:
            # Basic sanity check on response
            if isinstance(response_json, str):
                # Server returned plain string instead of JSON object
                return pd.DataFrame([{"Error": response_json}])

            if not isinstance(response_json, dict):
                return pd.DataFrame([{
                    "Error": f"Unexpected response type: {type(response_json)}"
                }])

            # Some backends may put data directly at top level,
            # others under "result"
            result = response_json.get("result", response_json)

            rows = []

            for ticker in tickers:
                ticker_data = result.get(ticker) if isinstance(result, dict) else None
                if ticker_data is None:
                    rows.append(pd.DataFrame([{
                        "Ticker": ticker,
                        "Parameter": None,
                        "Error": "No data for ticker"
                    }]))
                    continue

                for param in parameters:
                    # If ticker_data is not dict, we can't index by param
                    param_data = None
                    if isinstance(ticker_data, dict):
                        param_data = ticker_data.get(param)

                    if param_data is None:
                        rows.append(pd.DataFrame([{
                            "Ticker": ticker,
                            "Parameter": param,
                            "Error": "No prediction data available"
                        }]))
                        continue

                    # Handle both: dict with "data" key OR raw string
                    if isinstance(param_data, dict):
                        raw_data = param_data.get("data", "")
                    elif isinstance(param_data, str):
                        raw_data = param_data
                    else:
                        rows.append(pd.DataFrame([{
                            "Ticker": ticker,
                            "Parameter": param,
                            "Error": f"Unsupported data type: {type(param_data)}"
                        }]))
                        continue

                    if not raw_data:
                        rows.append(pd.DataFrame([{
                            "Ticker": ticker,
                            "Parameter": param,
                            "Error": "Empty prediction data"
                        }]))
                        continue

                    # Parse CSV-like content: first line header, rest data
                    lines = raw_data.strip().split('\n')
                    if len(lines) < 2:
                        rows.append(pd.DataFrame([{
                            "Ticker": ticker,
                            "Parameter": param,
                            "Error": "Insufficient data"
                        }]))
                        continue

                    data_rows = []
                    for line in lines[1:]:
                        parts = line.split()
                        if len(parts) >= 3:
                            data_rows.append({
                                "Date": parts[0],
                                "Time": parts[1],
                                "Predicted Price": float(parts[2])
                            })

                    if not data_rows:
                        rows.append(pd.DataFrame([{
                            "Ticker": ticker,
                            "Parameter": param,
                            "Error": "No valid data rows"
                        }]))
                        continue

                    df = pd.DataFrame(data_rows)
                    df["Ticker"] = ticker
                    rows.append(df[["Ticker", "Date", "Time", "Predicted Price"]])

            if rows:
                return pd.concat(rows, ignore_index=True)
            else:
                return pd.DataFrame([{"Error": "No data to display"}])

        except Exception as e:
            # last-resort safety
            return pd.DataFrame([{"Error": str(e)}])

    
    def get_prediction(self, tickers, time_frame, parameters, candle="1m"):
        # Normalize tickers
        if isinstance(tickers, str):
            tickers = [tickers]
        if not isinstance(tickers, list):
            return {"success": False, "error": "Tickers must be a string or list"}
        if len(tickers) > 3:
            return {"success": False, "error": "Maximum of 3 tickers allowed"}
        
        invalid_tickers = [t for t in tickers if t.upper() not in self.SUPPORTED_TICKERS]
        if invalid_tickers:
            error_msg = f"Ticker(s) not supported currently: {', '.join(invalid_tickers)}"
            print(f"❌ {error_msg}")
            print(f"\n✅ Supported tickers: {', '.join(sorted(self.SUPPORTED_TICKERS))}")
            return {"success": False, "error": error_msg}
        
        tickers = [t.upper() for t in tickers]

        if isinstance(parameters, str):
            parameters = [parameters]

        try:
            print("\n" + "="*60)
            print("Getting Predictions")
            print("="*60)
            
            token_check = self.token_manager.check_token_and_credits()
            if not token_check["valid"]:
                print(f"❌ {token_check['error']}")
                return {"success": False, "error": token_check["error"]}

            print(f"📊 Tickers: {', '.join(tickers)}")
            print(f"⏰ Time Frame: {time_frame}")
            print(f"🕒 Candle: {candle}")
            print(f"📈 Parameters: {', '.join(parameters)}")

            payload = {
                "action": {
                    "action_type": "predict",
                    "predict": {
                        "given": {
                            "ticker": tickers,
                            "time_frame": time_frame,
                            "candle": candle
                        },
                        "required": {
                            "parameters": parameters
                        }
                    }
                }
            }

            print("\n🔄 Fetching Predictions ...")
            response = requests.post(
                self.base_url,
                json=payload,
                headers={"X-Access-Token": self.access_token},
                timeout=300
            )
            response.raise_for_status()
            response_json = response.json()

            df = self._format_table(response_json, tickers, parameters)

            if self.token_manager.deduct_credit():
                remaining = self.token_manager.get_remaining_credits()
            else:
                remaining = 0

            print("\n" + "="*60)
            print(f"✅ Predictions ({time_frame}, candle={candle})")
            print("="*60)
            print(df.to_string(index=False))
            print("="*60)
            print(f"💳 Remaining credits: {remaining}")
            
            if remaining <= 10:
                print(f"⚠️  Warning: Only {remaining} credits remaining!")
            if remaining == 0:
                print("❌ Credits exhausted! Please subscribe to a plan to continue.")
            
            print("="*60)

            return {
                "success": True,
                "data": df,
                "credits_remaining": remaining,
                "timestamp": datetime.now().isoformat()
            }

        except requests.exceptions.Timeout:
            error_msg = "Request timed out. Please try again."
            print(f"❌ {error_msg}")
            return {"success": False, "error": error_msg}

        except requests.exceptions.RequestException as e:
            error_msg = f"API request failed: {str(e)}"
            print(f"❌ {error_msg}")
            return {"success": False, "error": error_msg}

        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            print(f"❌ {error_msg}")
            return {"success": False, "error": error_msg}

    def get_credits(self):
        """Get remaining credits for the current token"""
        credits = self.token_manager.get_remaining_credits()
        print(f"💳 Remaining credits: {credits}")
        return credits


# -------------- local test --------------
# if __name__ == "__main__":
#     client = Client(
#         access_token="sk_live_2df1613eca06f07cf0208f8ea30e0ce0f5a50c4a90b0f073321bce1c332e9da2"
#     )

#     result = client.get_prediction(
#         tickers=["ITC"],
#         time_frame="2 hours",
#         parameters=["close"],
#         candle="1m"
#     )

#     print("\nRAW RESULT DICT:")
#     print(result)
