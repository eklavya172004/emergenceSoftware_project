import React, { FC } from 'react'
import { experiences } from '../constants'
import { Button } from './ui/Moving-Border'
import Image from 'next/image'
import { styles } from '../data/style'

interface ExperienceCardType {
  id: number;
  title: string;
  company_name: string;
  icon: string;
  iconBg: string;
  date: string;
  points: string[];
}

const Experience: FC = () => {
  return (
    <div className="py-20" id="testimonials">
      <h2 className={styles.sectionHeadText}>
        My Experience
      </h2>

      <div className="w-full mt-12 grid lg:grid-cols-4 grid-cols-1 gap-10">
        {
          (experiences as ExperienceCardType[]).map((card) => (
            <Button key={card.id} duration={Math.floor(Math.random() * 10000) + 10000} borderRadius='1.75rem' className='flex-1 text-white border-neutral-200 dark:border-slate-800'>
              <div className='flex lg:flex-row flex-col lg:items-center p-3 py-6 md:p-5 lg:p-10 gap-2'>
                <Image src={card.icon} alt={card.title} width={128} height={128} className='lg:w-32 md:w-20 w-16' />
                <div className='lg:ms-5 '>
                  <h1 className='text-start text-xl md:text-2xl font-bold'>
                    {card.title}
                  </h1>

                  <p className='text-start text-slate-300 mt-3 font-semibold'>
                    {card.points}
                  </p>
                </div>
              </div>
            </Button>
          ))
        }
      </div>
    </div>
  )
}

export default Experience
