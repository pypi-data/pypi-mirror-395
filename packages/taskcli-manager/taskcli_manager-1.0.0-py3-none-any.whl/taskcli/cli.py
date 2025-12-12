#!/usr/bin/env python3
"""
TaskCLI - Interactive Command Line Interface
=============================================
A colorful, interactive CLI for managing tasks.
Connects to TaskCLI web API for data synchronization.

Usage:
    pip install taskcli-manager
    taskcli

Author: Ishita Tiwari
"""

import requests
import getpass
import os
import sys
from datetime import datetime

# API Base URL - Your Railway deployed app
API_URL = "https://ojtprojectrepo-production.up.railway.app"

# ANSI Color Codes
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

class TaskCLI:
    def __init__(self):
        self.current_user = None
        self.user_email = None
    
    def clear_screen(self):
        os.system('clear' if os.name != 'nt' else 'cls')
    
    def print_header(self):
        print(f"\n{Colors.CYAN}{Colors.BOLD}")
        print("╔══════════════════════════════════════════════════╗")
        print("║           🗓️  TASK CLI - Task Manager            ║")
        print("╚══════════════════════════════════════════════════╝")
        print(f"{Colors.END}")
        if self.current_user:
            print(f"{Colors.GREEN}👤 Logged in as: {self.current_user}{Colors.END}\n")
        else:
            print(f"{Colors.YELLOW}👤 Not logged in{Colors.END}\n")
    
    def print_auth_menu(self):
        print(f"\n{Colors.YELLOW}{Colors.BOLD}🔐 WELCOME{Colors.END}")
        print(f"{Colors.BLUE}{'─' * 50}{Colors.END}")
        print(f"  {Colors.GREEN} 1{Colors.END}. 🔑 Login")
        print(f"  {Colors.GREEN} 2{Colors.END}. 📝 Create New Account")
        print(f"  {Colors.GREEN} 0{Colors.END}. 🚪 Exit")
        print(f"{Colors.BLUE}{'─' * 50}{Colors.END}")
    
    def print_menu(self):
        print(f"\n{Colors.YELLOW}{Colors.BOLD}📋 MAIN MENU{Colors.END}")
        print(f"{Colors.BLUE}{'─' * 50}{Colors.END}")
        print(f"  {Colors.GREEN} 1{Colors.END}. 📄 View My Tasks")
        print(f"  {Colors.GREEN} 2{Colors.END}. ⏳ View Pending Tasks")
        print(f"  {Colors.GREEN} 3{Colors.END}. ✅ View Completed Tasks")
        print(f"  {Colors.GREEN} 4{Colors.END}. ➕ Add New Task")
        print(f"  {Colors.GREEN} 5{Colors.END}. ✔️  Mark Task as Complete")
        print(f"  {Colors.GREEN} 6{Colors.END}. ⏸️  Mark Task as Pending")
        print(f"  {Colors.GREEN} 7{Colors.END}. ✏️  Edit Task")
        print(f"  {Colors.GREEN} 8{Colors.END}. 🗑️  Delete Task")
        print(f"  {Colors.GREEN} 9{Colors.END}. 🔄 Logout")
        print(f"  {Colors.GREEN} 0{Colors.END}. 🚪 Exit")
        print(f"{Colors.BLUE}{'─' * 50}{Colors.END}")
    
    def get_input(self, prompt):
        try:
            return input(f"{Colors.CYAN}{prompt}{Colors.END}").strip()
        except (EOFError, KeyboardInterrupt):
            return None
    
    def login(self):
        print(f"\n{Colors.CYAN}{Colors.BOLD}🔑 LOGIN{Colors.END}")
        print(f"{Colors.BLUE}{'─' * 40}{Colors.END}")
        
        email = self.get_input("Email: ")
        if not email:
            return False
        
        password = getpass.getpass(f"{Colors.CYAN}Password: {Colors.END}")
        if not password:
            return False
        
        try:
            response = requests.post(f"{API_URL}/api/login/", json={
                "email": email,
                "password": password
            }, timeout=10)
            
            data = response.json()
            if data.get("success"):
                self.current_user = data.get("name")
                self.user_email = email
                print(f"\n{Colors.GREEN}✅ Welcome back, {self.current_user}!{Colors.END}")
                return True
            else:
                print(f"\n{Colors.RED}❌ {data.get('error', 'Login failed')}{Colors.END}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"\n{Colors.RED}❌ Connection error: {e}{Colors.END}")
            return False
    
    def signup(self):
        print(f"\n{Colors.CYAN}{Colors.BOLD}📝 CREATE NEW ACCOUNT{Colors.END}")
        print(f"{Colors.BLUE}{'─' * 40}{Colors.END}")
        
        name = self.get_input("Your Name: ")
        if not name:
            return False
        
        email = self.get_input("Email: ")
        if not email:
            return False
        
        password = getpass.getpass(f"{Colors.CYAN}Password (min 6 chars): {Colors.END}")
        if not password or len(password) < 6:
            print(f"\n{Colors.RED}❌ Password must be at least 6 characters{Colors.END}")
            return False
        
        try:
            response = requests.post(f"{API_URL}/api/signup/", json={
                "name": name,
                "email": email,
                "password": password
            }, timeout=10)
            
            data = response.json()
            if data.get("success"):
                self.current_user = data.get("name")
                self.user_email = email
                print(f"\n{Colors.GREEN}✅ Account created! Welcome, {self.current_user}!{Colors.END}")
                return True
            else:
                print(f"\n{Colors.RED}❌ {data.get('error', 'Signup failed')}{Colors.END}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"\n{Colors.RED}❌ Connection error: {e}{Colors.END}")
            return False
    
    def list_tasks(self, filter_type=None):
        try:
            response = requests.get(f"{API_URL}/api/tasks/", params={"email": self.user_email}, timeout=10)
            data = response.json()
            
            if not data.get("success"):
                print(f"{Colors.RED}❌ {data.get('error', 'Failed to fetch tasks')}{Colors.END}")
                return
            
            tasks = data.get("tasks", [])
            
            # Apply filter
            if filter_type == "pending":
                tasks = [t for t in tasks if not t["completed"]]
            elif filter_type == "completed":
                tasks = [t for t in tasks if t["completed"]]
            
            if not tasks:
                print(f"{Colors.YELLOW}⚠️ No tasks found.{Colors.END}")
                return
            
            print(f"\n{Colors.BOLD}{'ID':<5} {'Name':<22} {'Project':<12} {'Priority':<8} {'Due':<12} {'Status'}{Colors.END}")
            print(f"{Colors.BLUE}{'─' * 75}{Colors.END}")
            
            for task in tasks:
                status_icon = f"{Colors.GREEN}✅" if task["completed"] else f"{Colors.YELLOW}⏳"
                priority_color = Colors.RED if task["priority"] == 'High' else (Colors.YELLOW if task["priority"] == 'Medium' else Colors.GREEN)
                
                name = task["name"][:19] + "..." if len(task["name"]) > 22 else task["name"]
                project = task["project"][:9] + "..." if len(task["project"]) > 12 else task["project"]
                
                print(f"{task['id']:<5} {name:<22} {project:<12} {priority_color}{task['priority']:<8}{Colors.END} {task['due_date']:<12} {status_icon}{Colors.END}")
            
            print(f"\n{Colors.CYAN}Total: {len(tasks)} task(s){Colors.END}")
            
        except requests.exceptions.RequestException as e:
            print(f"{Colors.RED}❌ Connection error: {e}{Colors.END}")
    
    def add_task(self):
        print(f"\n{Colors.CYAN}{Colors.BOLD}➕ ADD NEW TASK{Colors.END}")
        print(f"{Colors.BLUE}{'─' * 40}{Colors.END}")
        
        name = self.get_input("Task name: ")
        if not name:
            print(f"{Colors.RED}❌ Task name is required.{Colors.END}")
            return
        
        project = self.get_input("Project (default: General): ") or "General"
        
        print(f"\n{Colors.YELLOW}Priority:{Colors.END}")
        print("  1. High  2. Medium  3. Low")
        priority_choice = self.get_input("Select (1-3): ") or "2"
        priority_map = {'1': 'High', '2': 'Medium', '3': 'Low'}
        priority = priority_map.get(priority_choice, 'Medium')
        
        due_date = self.get_input(f"Due date (YYYY-MM-DD, default: today): ") or datetime.now().strftime('%Y-%m-%d')
        due_time = self.get_input("Due time (HH:MM, default: 12:00): ") or "12:00"
        
        try:
            response = requests.post(f"{API_URL}/api/tasks/add/", json={
                "email": self.user_email,
                "name": name,
                "project": project,
                "priority": priority,
                "due_date": due_date,
                "due_time": due_time
            }, timeout=10)
            
            data = response.json()
            if data.get("success"):
                print(f"{Colors.GREEN}✅ Task '{name}' created with ID {data.get('task_id')}{Colors.END}")
            else:
                print(f"{Colors.RED}❌ {data.get('error', 'Failed to create task')}{Colors.END}")
        except requests.exceptions.RequestException as e:
            print(f"{Colors.RED}❌ Connection error: {e}{Colors.END}")
    
    def complete_task(self):
        print(f"\n{Colors.CYAN}{Colors.BOLD}✔️ MARK TASK AS COMPLETE{Colors.END}")
        self.list_tasks("pending")
        task_id = self.get_input("\nEnter Task ID to complete: ")
        
        if task_id:
            try:
                response = requests.post(f"{API_URL}/api/tasks/{task_id}/complete/", timeout=10)
                data = response.json()
                if data.get("success"):
                    print(f"{Colors.GREEN}✅ Task {task_id} marked as complete!{Colors.END}")
                else:
                    print(f"{Colors.RED}❌ {data.get('error', 'Failed')}{Colors.END}")
            except:
                print(f"{Colors.RED}❌ Connection error{Colors.END}")
    
    def pending_task(self):
        print(f"\n{Colors.CYAN}{Colors.BOLD}⏸️ MARK TASK AS PENDING{Colors.END}")
        self.list_tasks("completed")
        task_id = self.get_input("\nEnter Task ID to mark pending: ")
        
        if task_id:
            try:
                response = requests.post(f"{API_URL}/api/tasks/{task_id}/pending/", timeout=10)
                data = response.json()
                if data.get("success"):
                    print(f"{Colors.YELLOW}⏳ Task {task_id} marked as pending.{Colors.END}")
                else:
                    print(f"{Colors.RED}❌ {data.get('error', 'Failed')}{Colors.END}")
            except:
                print(f"{Colors.RED}❌ Connection error{Colors.END}")
    
    def edit_task(self):
        print(f"\n{Colors.CYAN}{Colors.BOLD}✏️ EDIT TASK{Colors.END}")
        self.list_tasks()
        task_id = self.get_input("\nEnter Task ID to edit: ")
        
        if not task_id:
            return
        
        print(f"\n{Colors.YELLOW}Enter new values (press Enter to skip):{Colors.END}")
        name = self.get_input("New name: ")
        project = self.get_input("New project: ")
        priority = self.get_input("New priority (High/Medium/Low): ")
        due_date = self.get_input("New due date (YYYY-MM-DD): ")
        
        update_data = {}
        if name: update_data["name"] = name
        if project: update_data["project"] = project
        if priority: update_data["priority"] = priority
        if due_date: update_data["due_date"] = due_date
        
        if update_data:
            try:
                response = requests.post(f"{API_URL}/api/tasks/{task_id}/edit/", json=update_data, timeout=10)
                data = response.json()
                if data.get("success"):
                    print(f"{Colors.GREEN}✅ Task {task_id} updated!{Colors.END}")
                else:
                    print(f"{Colors.RED}❌ {data.get('error', 'Failed')}{Colors.END}")
            except:
                print(f"{Colors.RED}❌ Connection error{Colors.END}")
    
    def delete_task(self):
        print(f"\n{Colors.CYAN}{Colors.BOLD}🗑️ DELETE TASK{Colors.END}")
        self.list_tasks()
        task_id = self.get_input("\nEnter Task ID to delete: ")
        
        if task_id:
            confirm = self.get_input(f"{Colors.RED}Are you sure? (yes/no): {Colors.END}")
            if confirm and confirm.lower() in ['yes', 'y']:
                try:
                    response = requests.post(f"{API_URL}/api/tasks/{task_id}/delete/", timeout=10)
                    data = response.json()
                    if data.get("success"):
                        print(f"{Colors.GREEN}✅ Task {task_id} deleted.{Colors.END}")
                    else:
                        print(f"{Colors.RED}❌ {data.get('error', 'Failed')}{Colors.END}")
                except:
                    print(f"{Colors.RED}❌ Connection error{Colors.END}")
            else:
                print(f"{Colors.YELLOW}Deletion cancelled.{Colors.END}")
    
    def run(self):
        self.clear_screen()
        self.print_header()
        
        # Auth menu
        while not self.current_user:
            self.print_auth_menu()
            choice = self.get_input("Enter your choice: ")
            
            if choice is None or choice == '0':
                print(f"\n{Colors.GREEN}👋 Goodbye!{Colors.END}\n")
                return
            elif choice == '1':
                if self.login():
                    input("\nPress Enter to continue...")
                    break
            elif choice == '2':
                if self.signup():
                    input("\nPress Enter to continue...")
                    break
            else:
                print(f"{Colors.RED}❌ Invalid choice.{Colors.END}")
            
            input("\nPress Enter to continue...")
            self.clear_screen()
            self.print_header()
        
        self.clear_screen()
        self.print_header()
        
        # Main menu
        while True:
            self.print_menu()
            choice = self.get_input("Enter your choice: ")
            
            if choice is None or choice == '0':
                print(f"\n{Colors.GREEN}👋 Goodbye! Thanks for using TaskCLI!{Colors.END}\n")
                break
            elif choice == '1':
                self.list_tasks()
            elif choice == '2':
                self.list_tasks("pending")
            elif choice == '3':
                self.list_tasks("completed")
            elif choice == '4':
                self.add_task()
            elif choice == '5':
                self.complete_task()
            elif choice == '6':
                self.pending_task()
            elif choice == '7':
                self.edit_task()
            elif choice == '8':
                self.delete_task()
            elif choice == '9':
                self.current_user = None
                self.user_email = None
                self.clear_screen()
                self.print_header()
                continue
            else:
                print(f"{Colors.RED}❌ Invalid choice.{Colors.END}")
            
            input("\nPress Enter to continue...")
            self.clear_screen()
            self.print_header()

def main():
    cli = TaskCLI()
    cli.run()

if __name__ == "__main__":
    main()
