testcases = [
  {
    "TestCaseID": "TC_HPX_001",
    "Module": "Login",
    "TestCaseName": "Valid Login",
    "Description": "Verify login with valid credentials",
    "Steps": "Open app > Enter username/password > Click login",
    "ExpectedResult": "User should login successfully",
    "Priority": "High",
    "Status": "Pass",
    "CreatedBy": "Omkar",
    "ExecutionDate": "2026-04-08"
  },
  {
    "TestCaseID": "TC_HPX_002",
    "Module": "Login",
    "TestCaseName": "Invalid Login",
    "Description": "Verify login with invalid password",
    "Steps": "Open app > Enter wrong password > Click login",
    "ExpectedResult": "Error message should display",
    "Priority": "High",
    "Status": "Fail",
    "CreatedBy": "Omkar",
    "ExecutionDate": "2026-04-08"
  },
  {
    "TestCaseID": "TC_HPX_003",
    "Module": "Dashboard",
    "TestCaseName": "Load Dashboard",
    "Description": "Verify dashboard loads properly",
    "Steps": "Login > Navigate to dashboard",
    "ExpectedResult": "Dashboard should load without errors",
    "Priority": "Medium",
    "Status": "Pass",
    "CreatedBy": "Omkar",
    "ExecutionDate": "2026-04-08"
  },
  {
    "TestCaseID": "TC_HPX_004",
    "Module": "Search",
    "TestCaseName": "Search Product",
    "Description": "Verify product search functionality",
    "Steps": "Enter keyword in search bar > Click search",
    "ExpectedResult": "Relevant results should display",
    "Priority": "Medium",
    "Status": "Pass",
    "CreatedBy": "Omkar",
    "ExecutionDate": "2026-04-08"
  },
  {
    "TestCaseID": "TC_HPX_005",
    "Module": "Cart",
    "TestCaseName": "Add to Cart",
    "Description": "Verify adding item to cart",
    "Steps": "Select product > Click add to cart",
    "ExpectedResult": "Item should be added to cart",
    "Priority": "High",
    "Status": "Pass",
    "CreatedBy": "Omkar",
    "ExecutionDate": "2026-04-08"
  },
  {
    "TestCaseID": "TC_HPX_006",
    "Module": "Cart",
    "TestCaseName": "Remove from Cart",
    "Description": "Verify removing item from cart",
    "Steps": "Go to cart > Click remove",
    "ExpectedResult": "Item should be removed",
    "Priority": "Medium",
    "Status": "Pass",
    "CreatedBy": "Omkar",
    "ExecutionDate": "2026-04-08"
  },
  {
    "TestCaseID": "TC_HPX_007",
    "Module": "Checkout",
    "TestCaseName": "Successful Checkout",
    "Description": "Verify checkout process",
    "Steps": "Add item > Go to checkout > Enter details > Place order",
    "ExpectedResult": "Order should be placed successfully",
    "Priority": "High",
    "Status": "Pass",
    "CreatedBy": "Omkar",
    "ExecutionDate": "2026-04-08"
  },
  {
    "TestCaseID": "TC_HPX_008",
    "Module": "Checkout",
    "TestCaseName": "Payment Failure",
    "Description": "Verify failed payment scenario",
    "Steps": "Add item > Checkout > Enter invalid payment details",
    "ExpectedResult": "Payment failure message should display",
    "Priority": "High",
    "Status": "Fail",
    "CreatedBy": "Omkar",
    "ExecutionDate": "2026-04-08"
  },
  {
    "TestCaseID": "TC_HPX_009",
    "Module": "Profile",
    "TestCaseName": "Update Profile",
    "Description": "Verify profile update",
    "Steps": "Go to profile > Edit details > Save",
    "ExpectedResult": "Profile should update successfully",
    "Priority": "Low",
    "Status": "Pass",
    "CreatedBy": "Omkar",
    "ExecutionDate": "2026-04-08"
  },
  {
    "TestCaseID": "TC_HPX_010",
    "Module": "Logout",
    "TestCaseName": "Logout Functionality",
    "Description": "Verify logout",
    "Steps": "Click logout",
    "ExpectedResult": "User should be logged out",
    "Priority": "High",
    "Status": "Pass",
    "CreatedBy": "Omkar",
    "ExecutionDate": "2026-04-08"
  }
]

import json
with open('testcases.json', 'w') as f:
    json.dump({"testcases": testcases}, f, indent=2)
