import {
  mobile,
  backend,
  creator,
  web,
  javascript,
  typescript,
  html,
  css,
  reactjs,
  redux,
  tailwind,
  nodejs,
  mongodb,
  git,
  figma,
  docker,
  meta,
  starbucks,
  tesla,
  shopify,
  carrent,
  jobit,
  tripguide,
  threejs,
} from "../../public/assets";

import { StaticImageData } from 'next/image';

// Type Definitions
export interface Service {
  title: string;
  icon: string | StaticImageData;
}

export interface Technology {
  name: string;
  icon: string | StaticImageData;
}

export interface Experience {
  id: number;
  title: string;
  company_name: string;
  icon: string | StaticImageData;
  iconBg: string;
  date: string;
  points: string[];
}

export interface Project {
  id: number;
  title: string;
  description: string;
  tags: string[];
  image: string | StaticImageData;
  source_code_link: string;
  preview: string;
}

export interface Testimonial {
  testimonial: string;
  name: string;
  designation: string;
  company: string;
  image: string;
}

export interface NavLink {
  id: string;
  title: string;
}

export const navLinks: NavLink[] = [
  {
    id: "about",
    title: "About",
  },
  {
    id: "work",
    title: "Work",
  },
  {
    id: "contact",
    title: "Contact",
  },
];

const services: Service[] = [
  {
    title: "Web Developer",
    icon: web.src || web,
  },
  {
    title: "Problem Solver",
    icon: mobile.src || mobile,
  },
  {
    title: "Backend Developer",
    icon: backend.src || backend,
  },
  {
    title: "Generative AI Expert",
    icon: creator.src || creator,
  },
];

const technologies: Technology[] = [
  {
    name: "HTML 5",
    icon: html.src || html,
  },
  {
    name: "CSS 3",
    icon: css.src || css,
  },
  {
    name: "JavaScript",
    icon: javascript.src || javascript,
  },
  {
    name: "TypeScript",
    icon: typescript.src || typescript,
  },
  {
    name: "React JS",
    icon: reactjs.src || reactjs,
  },
  {
    name: "Redux Toolkit",
    icon: redux.src || redux,
  },
  {
    name: "Tailwind CSS",
    icon: tailwind.src || tailwind,
  },
  {
    name: "Node JS",
    icon: nodejs.src || nodejs,
  },
  {
    name: "MongoDB",
    icon: mongodb.src || mongodb,
  },
  {
    name: "Three JS",
    icon: threejs.src || threejs,
  },
  {
    name: "git",
    icon: git.src || git,
  },
  {
    name: "figma",
    icon: figma.src || figma,
  },
  {
    name: "docker",
    icon: docker.src || docker,
  },
];

const experiences: Experience[] = [
  {
    id: 1,
    title: "React Developer",
    company_name: "Artigence Healthcare",
    icon: starbucks.src || starbucks,
    iconBg: "#383E56",
    date: "April 2025 - June 2025",
    points: [
      "Developed responsive healthcare management interfaces using React.js and Tailwind CSS.",
      "Integrated RESTful APIs and implemented data visualization components for patient monitoring.",
      "Built AI-powered dashboard features using React and TensorFlow.js for real-time patient data analysis.",
      "Participated in Agile development process with daily stand-ups and sprint planning.",
    ],
  },
  {
    id: 2,
    title: "Tech Lead",
    company_name: "Surge Sports Fest",
    icon: tesla.src || tesla,
    iconBg: "#E6DEDD",
    date: "Jan 2024 - Apr 2024",
    points: [
      "Architected and deployed production-ready sports event platform supporting multiple sports with flexible team-based registration system.",
      "Built intuitive user dashboard enabling seamless team creation, registration tracking, and real-time event participation management.",
      "Integrated secure payment gateway with real-time transaction status updates and automated confirmation emails.",
      "Created comprehensive admin panel using Retool for efficient registration management, payment verification, and complete CRUD operations.",
      "Implemented fully responsive design ensuring optimal user experience across all devices and screen sizes.",
    ],
  },
];

const testimonials: Testimonial[] = [
  {
    testimonial:
      "I thought it was impossible to make a website as beautiful as our product, but Rick proved me wrong.",
    name: "Sara Lee",
    designation: "CFO",
    company: "Acme Co",
    image: "https://randomuser.me/api/portraits/women/4.jpg",
  },
  {
    testimonial:
      "I've never met a web developer who truly cares about their clients' success like Rick does.",
    name: "Chris Brown",
    designation: "COO",
    company: "DEF Corp",
    image: "https://randomuser.me/api/portraits/men/5.jpg",
  },
  {
    testimonial:
      "After Rick optimized our website, our traffic increased by 50%. We can't thank them enough!",
    name: "Lisa Wang",
    designation: "CTO",
    company: "456 Enterprises",
    image: "https://randomuser.me/api/portraits/women/6.jpg",
  },
];

const projects: Project[] = [
  {
    id: 1,
    title: "CakeShop",
    description:
      "AI-Powered Multi-Vendor E-Commerce Platform built with Next.js, TypeScript, Prisma, and PostgreSQL. Features include AI-generated cake designs via OpenAI API, role-based access control, real-time analytics dashboards for admins and vendors, secure NextAuth authentication, Razorpay payment gateway with split payouts, and scalable REST APIs for complete e-commerce functionality.",
    tags: ["All", "Fullstack"],
    image: "/images/cake-shop.jpg",
    source_code_link: "https://github.com/eklavya172004/Cake-Website-",
    preview: "https://purblepalace.in/",
  },
  {
    id: 2,
    title: "SurgeSNU",
    description:
      "Production-ready Sports Event Management Platform with beautiful frontend animations and comprehensive functionality. Supports multi-sport team-based registrations, intuitive user dashboard for team creation and event tracking, integrated payment gateway with real-time updates, admin panel built with Retool for registration and payment management, and fully responsive design optimized for all devices.",
    tags: ["All", "Fullstack"],
    image: "/images/surgesnu.png",
    source_code_link: "https://github.com/eklavya172004/Surge-website-2025",
    preview: "https://surgesnu.in/",
  },
  {
    id: 3,
    title: "CodeSphere",
    description:
      "Modern and responsive frontend project showcasing clean UI/UX design principles, interactive components, and smooth animations. Built with a focus on user experience and visual appeal.",
    tags: ["All", "Frontend"],
    image: "/images/codespehere.jpg",
    source_code_link: "https://github.com/eklavya172004/frontend-of-codesphere",
    preview: "https://frontend-of-codesphere-7vx2.vercel.app/",
  },
];

export { services, technologies, experiences, testimonials, projects };
