#!/usr/bin/env python3
"""
Easy script to update your resume for the chat AI.
Simply edit the resume content below and run this script.
"""

import httpx
import json

# ============================================
# EDIT YOUR RESUME BELOW
# ============================================

YOUR_RESUME = """
EKLAVYA NATH
Indore, Madhya Pradesh, India
Email: en956@snu.edu.in
Phone: +91-9522494683
LinkedIn | GitHub | LeetCode | Codeforces

PROFESSIONAL SUMMARY
Full-stack developer with expertise in frontend, backend, and database technologies. Experienced in building scalable web applications with AI integration. Strong problem-solving skills with 350+ problems solved on LeetCode and active participation in competitive programming.

EDUCATION

Shiv Nadar University — B.Tech in Computer Science Engineering (ongoing)
Aug 2023 – May 2027
CGPA: 7.53/10.0

Bansal Public School, Kota, Rajasthan — Class XII (CBSE) - (school)
2020 – 2022
Percentage: 78%

St. Mary’s Convent School, Ujjain, Madhya Pradesh — Class X (CBSE) - (school)
2019 – 2020
Percentage: 90%

TECHNICAL SKILLS

Programming Languages:
- C++
- JavaScript
- Python

Frontend:
- React.js
- Next.js
- HTML5
- CSS3
- Tailwind CSS
- TypeScript
- Figma

Backend:
- Node.js
- Express.js
- RESTful APIs
- NextAuth
- JWT

Databases:
- MongoDB
- PostgreSQL
- MySQL
- Prisma ORM

Tools & Technologies:
- Git
- GitHub
- GSAP
- Retool
- Docker
- AWS

WORK EXPERIENCE

React Developer Intern — Artigence Healthcare
April 2025 – June 2025

- Developed responsive healthcare management interfaces using React.js and Tailwind CSS
- Integrated RESTful APIs and implemented data visualization components for patient monitoring
- Built AI-powered dashboard features using React and TensorFlow.js for real-time patient data analysis
- Participated in Agile development process with daily stand-ups and sprint planning
- Received internship completion certificate

PROJECTS

1. CakeShop — AI-Powered Multi-Vendor E-Commerce Platform
Deployed Website Available

- Built full-stack multi-vendor platform using Next.js, TypeScript, Prisma, and PostgreSQL with role-based access control for Admin, Vendor, and Customer roles
- Integrated OpenAI API to generate customized cake designs and descriptions based on user preferences
- Developed admin and vendor dashboards with real-time analytics, order management, and revenue tracking
- Implemented secure authentication using NextAuth, JWT, and bcrypt with vendor verification workflow
- Integrated Razorpay payment gateway with split payouts, refunds, and webhook event handling
- Designed scalable REST APIs for products, orders, analytics, disputes, and promotional campaigns
- Integrated email notification services

2. SurgeSNU — Sports Event Management Platform
Deployed Website Available

- Developed production-ready sports event platform with team-based registrations across multiple sports
- Built user dashboard for team creation, registration tracking, and event participation management
- Integrated payment gateway with real-time status updates and confirmation emails
- Created admin panel using Retool for registration management, payment verification, and CRUD operations
- Implemented responsive design for seamless experience across desktop and mobile devices
- Led development as Tech Lead at Surge Sports Fest

ACHIEVEMENTS

- Solved 350+ problems on LeetCode focused on Data Structures and Algorithms
- Achieved 900+ rating on Codeforces competitive programming platform
- Tech Lead for full-stack sports management platform at Surge Sports Fest

LANGUAGES & SOFT SKILLS

Languages:
- English
- Hindi

Soft Skills:
- Strong problem-solving ability
- Analytical thinking
- Team collaboration
- Agile development experience
- Leadership experience as Tech Lead
"""

# ============================================
# API CONFIGURATION
# ============================================

API_URL = "http://localhost:8000/api/v1/chat/update-resume"

# ============================================
# UPDATE RESUME
# ============================================

def update_resume():
    """Update the resume in the backend."""
    try:
        payload = {
            "resume_content": YOUR_RESUME.strip()
        }
        
        response = httpx.post(
            API_URL,
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Resume updated successfully!")
            print(f"Response: {result['message']}")
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Details: {response.text}")
            return False
            
    except httpx.ConnectError:
        print("❌ Error: Cannot connect to backend")
        print("Make sure the backend is running: python main.py")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def verify_resume():
    """Verify the resume was updated."""
    try:
        response = httpx.get("http://localhost:8000/api/v1/chat/resume")
        
        if response.status_code == 200:
            data = response.json()
            resume = data.get("resume_content", "")
            print("\n📄 Current Resume Content:")
            print("=" * 50)
            print(resume[:500] + "..." if len(resume) > 500 else resume)
            print("=" * 50)
            return True
        else:
            print("❌ Could not verify resume")
            return False
            
    except Exception as e:
        print(f"❌ Error verifying: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Resume Chat AI - Resume Updater")
    print("=" * 50)
    print()
    
    if update_resume():
        print()
        print("✨ Your resume is now loaded in the AI!")
        print()
        print("Next steps:")
        print("1. Go to http://localhost:3000/chat")
        print("2. Enter your name")
        print("3. Ask questions like:")
        print("   - 'What are your technical skills?'")
        print("   - 'Tell me about the AI Portfolio Chat project'")
        print("   - 'What experience do you have with React?'")
        print()
        print("Verify your resume was updated:")
        verify_resume()
    else:
        print()
        print("⚠️ Make sure:")
        print("1. Backend is running: cd backend && python main.py")
        print("2. Environment is configured correctly")
        print("3. Try again in a moment")
