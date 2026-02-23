'use client'
import React, { FC, useState, ChangeEvent, FormEvent } from 'react'
import { SocialIcon } from 'react-social-icons'
import { useToast } from './Toast'

interface FormData {
  email: string;
  subject: string;
  message: string;
}

const EmailSection: FC = () => {
  const { addToast } = useToast();
  const [formData, setFormData] = useState<FormData>({
    email: '',
    subject: '',
    message: ''
  });
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleInputChange = (e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>): void => {
    const { id, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [id]: value
    }));
  };

  const handleSubmit = (e: FormEvent<HTMLFormElement>): void => {
    e.preventDefault();
    setIsSubmitting(true);

    const recipientEmail = "eklavyanath172004@gmail.com";
    const encodedSubject = encodeURIComponent(formData.subject);
    const encodedBody = encodeURIComponent(
      `From: ${formData.email}\n\nMessage:\n${formData.message}`
    );

    // Show success toast
    addToast({
      type: 'success',
      message: '✓ Message prepared! Opening your email client...',
      duration: 3000
    });

    // Clear the form
    setFormData({
      email: '',
      subject: '',
      message: ''
    });

    // Open mailto after a short delay
    setTimeout(() => {
      const mailtoLink = `mailto:${recipientEmail}?subject=${encodedSubject}&body=${encodedBody}`;
      window.location.href = mailtoLink;
      setIsSubmitting(false);
    }, 500);
  };

  return (
    <section id="contact" className='grid md:grid-cols-2 grid-cols-1 my-12 md:my-12 py-24 gap-4 text-white '>
      <div className="bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-purple-900 to-transparent rounded-full h-80 w-80 z-0 blur-lg absolute top-3/4 -left-4 transform -translate-x-1/2 -translate-1/2"></div>

      <div className='z-10'>
        <h2 className='text-xl font-bold text-white my-2'>
          Let&#39;s Connect
        </h2>
        <p className='text-[#ADB7BE] mb-4 max-w-md'>
          {" "}
          I&apos;d love to hear from you! Whether you have a project in mind, want to collaborate, or just want to chat about technology and development, feel free to reach out through email or connect with me on my social profiles.
        </p>
        <div className='social-links flex flex-row gap-2'>
          <SocialIcon target='_blank' url="https://github.com/eklavya172004" />
          <SocialIcon target='_blank' url="https://www.linkedin.com/in/eklavya-nath-506818286/" />
          <SocialIcon target='_blank' url="https://leetcode.com/u/eklavya172004/" />
        </div>
      </div>

      <div>
        <form className='flex flex-col' onSubmit={handleSubmit}>
          <div className='mb-6'>
            <label htmlFor="email" className='text-white block mb-2 text-sm font-medium'>Your email</label>
            <input
              type="email"
              id='email'
              required
              className='bg-[#18191E] border border-[#33353F] placeholder-[#9CA2A9] text-gray-100 text-sm block w-full p-3 rounded-lg'
              placeholder='your-email@google.com'
              value={formData.email}
              onChange={handleInputChange}
            />
          </div>

          <div className='mb-6'>
            <label htmlFor="subject" className='text-white block mb-2 text-sm font-medium'>Subject</label>
            <input
              type="text"
              id='subject'
              required
              className='bg-[#18191E] border border-[#33353F] placeholder-[#9CA2A9] text-gray-100 text-sm block w-full p-3 rounded-lg'
              placeholder='Subject'
              value={formData.subject}
              onChange={handleInputChange}
            />
          </div>

          <div className='mb-6'>
            <label htmlFor="message" className='text-white block text-sm mb-2 font-medium'>
              Your message
            </label>
            <textarea
              id="message"
              required
              className='bg-[#18191E] border border-[#33353F] placeholder-[#9CA2A9] text-gray-100 text-sm block w-full p-3 rounded-lg'
              placeholder='Let me know your thoughts'
              value={formData.message}
              onChange={handleInputChange}
            ></textarea>
          </div>
          <button 
            type='submit' 
            disabled={isSubmitting}
            className='bg-purple-500 hover:bg-purple-600 disabled:bg-purple-400 disabled:cursor-not-allowed text-white font-medium py-3 px-5 rounded-lg w-full transition duration-200'
          >
            {isSubmitting ? '⏳ Sending...' : '📧 Send Message'}
          </button>
        </form>
      </div>
    </section>
  );
}

export default EmailSection;
