import React, { useState, ChangeEvent, FormEvent } from 'react';

export interface ProfileFormValues {
  firstName: string;
  lastName: string;
  email: string;
  urls: string[];
  resume: File | null;
  interests: string[];
}

interface FormProps {
    onSubmit: (formData: ProfileFormValues) => void;
  }

const Form: React.FC<FormProps> = ({ onSubmit }) => {
  const [formValues, setFormValues] = useState<ProfileFormValues>({
    firstName: '',
    lastName: '',
    email: '',
    urls: [''],
    resume: null,
    interests: [],
  });

  const [newInterest, setNewInterest] = useState('');
  const [resumeFileName, setResumeFileName] = useState('');

  const handleInputChange = (e: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormValues({ ...formValues, [name]: value });
  };

  const handleUrlChange = (index: number, value: string) => {
    const updatedUrls = [...formValues.urls];
    updatedUrls[index] = value;
    setFormValues({ ...formValues, urls: updatedUrls });
  };

  const handleAddUrl = () => {
    setFormValues({ ...formValues, urls: [...formValues.urls, ''] });
  };

  const handleRemoveUrl = (index: number) => {
    const updatedUrls = formValues.urls.filter((_, i) => i !== index);
    setFormValues({ ...formValues, urls: updatedUrls });
  };

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFormValues({ ...formValues, resume: e.target.files[0] });
      setResumeFileName(e.target.files[0].name);
    }
  };

  const handleAddInterest = () => {
    if (newInterest.trim() && !formValues.interests.includes(newInterest.trim())) {
      setFormValues({
        ...formValues,
        interests: [...formValues.interests, newInterest.trim()],
      });
      setNewInterest('');
    }
  };

  const handleRemoveInterest = (interest: string) => {
    setFormValues({
      ...formValues,
      interests: formValues.interests.filter((i) => i !== interest),
    });
  };

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    onSubmit(formValues); // Pass form data to parent component
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="border border-white text-white p-8 rounded-lg shadow-lg max-w-xl mx-auto"
    >

<div className="flex gap-4 mb-4">
  {/* First Name */}
  <input
    type="text"
    name="firstName"
    value={formValues.firstName}
    onChange={handleInputChange}
    placeholder="First Name"
    className="flex-1 p-3 rounded-lg bg-black border-white border-2"
    required
  />

  {/* Last Name */}
  <input
    type="text"
    name="lastName"
    value={formValues.lastName}
    onChange={handleInputChange}
    placeholder="Last Name"
    className="flex-1 p-3 rounded-lg bg-black border-white border-2"
    required
  />
</div>

      {/* Email */}
      <input
        type="email"
        name="email"
        value={formValues.email}
        onChange={handleInputChange}
        placeholder="Email"
        className="w-full p-3 mb-4 rounded-lg bg-black border-white border-2"
        required
      />

      {/* URLs */}
      <label className="block mb-4">
        <span className="block mb-2">Add Your URLs:</span>
        {formValues.urls.map((url, index) => (
          <div key={index} className="flex items-center mb-3">
            <input
              type="url"
              value={url}
              onChange={(e) => handleUrlChange(index, e.target.value)}
              placeholder="Github, Projects or LinkedIn"
              className="w-full p-3 rounded-lg bg-black border-white border-2"
            />
            {formValues.urls.length > 1 && (
              <button
                type="button"
                onClick={() => handleRemoveUrl(index)}
                className="ml-3 text-red-500"
              >
                &times;
              </button>
            )}
          </div>
        ))}
        <button
          type="button"
          onClick={handleAddUrl}
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg mt-2"
        >
          Add URL
        </button>
      </label>

      {/* Resume Upload */}
      <label className="block mb-6">
        <span className="block mb-2">Upload Resume:</span>
        <input
          type="file"
          onChange={handleFileChange}
          className="text-white"
          accept=".pdf,.doc,.docx"
        />
        {resumeFileName && <p className="mt-2">Selected: {resumeFileName}</p>}
      </label>

      {/* Interests Input */}
      <div className="mb-6">
        <input
          type="text"
          value={newInterest}
          onChange={(e) => setNewInterest(e.target.value)}
          placeholder="Add an interest (e.g., React, Python it can also be Pokemon)"
          className="w-full p-3 mb-2 rounded-lg bg-black border-white border-2"
        />
        <button
          type="button"
          onClick={handleAddInterest}
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg"
        >
          Add Interest
        </button>
        {formValues.interests.length < 3 && (
        <p className="text-red-500 text-sm mt-2">At least 3 interests are required to run the algorithm</p>
        )}
      </div>

      {/* Display Interests */}
      <div className="mb-6">
        {formValues.interests.map((interest, index) => (
          <span
            key={index}
            className="inline-block bg-blue-500 text-white px-3 py-1 rounded-full mr-2 mb-2"
          >
            {interest}
            <button
              type="button"
              onClick={() => handleRemoveInterest(interest)}
              className="ml-2 text-red-400"
            >
              &times;
            </button>
          </span>
        ))}
      </div>

      {/* Submit Button */}
      <button
  type="submit"
  className="w-full bg-purple-500 hover:bg-green-700 text-white py-3 rounded-lg font-bold"
  disabled={
    formValues.interests.length <= 2 // Add your other required field checks here
  }
>
  Submit
</button>
    </form>
  );
};

export default Form;
