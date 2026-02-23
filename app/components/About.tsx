'use client';
import React, { FC } from "react";
import Image from "next/image";
import { StaticImageData } from "next/image";
import Tilt from 'react-parallax-tilt';
import { motion } from "framer-motion";
import { styles } from "../data/style";
import { services } from "../constants";
import { fadeIn, textVariant } from "../utils/motion";

interface ServiceCardProps {
  index: number;
  title: string;
  icon: string | StaticImageData;
}

const ServiceCard: FC<ServiceCardProps> = ({ index, title, icon }) => (
    <Tilt 
        className="xs:w-[250px] w-full"
        tiltMaxAngleX={20}
        tiltMaxAngleY={20}
        scale={1}
        transitionSpeed={450}
    >
        <motion.div 
            variants={fadeIn("right", "spring", index * 0.5, 0.75)} 
            initial="hidden"
            animate="show"
            className="w-full green-pink-gradient p-[1px] rounded-[20px] shadow-card"
        >
            <div className="bg-[#151030] rounded-[20px] py-5 px-12 min-h-[280px] flex justify-evenly items-center flex-col">
                <Image src={icon} alt={title} width={64} height={64} className="w-16 h-16 object-contain"/>
                <h3 className="text-white text-[20px] font-bold text-center">
                    {title}
                </h3>
            </div>
        </motion.div>
    </Tilt>
)

const About: FC = () => (
    <div id="about">
        <motion.div>
            <h2 className={styles.sectionHeadText}>
                Overview
            </h2>
        </motion.div>

        <motion.p
            variants={fadeIn("", "spring", 0.1, 1)}
            initial="hidden"
            animate="show"
            className="mt-4 text-[#aaa6c3] text-[17px] max-w-3xl leading-[30px]"
        >
            Full-stack developer with expertise in frontend, backend, and database technologies. I specialize in building scalable web applications with AI integration, combining modern technologies with strong problem-solving skills. With 350+ problems solved on LeetCode and a 900+ Codeforces rating, I bring both practical development experience and competitive programming excellence to every project. Currently pursuing B.Tech in Computer Science at Shiv Nadar University.
        </motion.p>

        <div className="mt-20 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-2 gap-10">
            {services.map((service, index) => (
                <ServiceCard key={service.title} index={index} {...service} />
            ))}
        </div>
    </div>
)

export default About;
