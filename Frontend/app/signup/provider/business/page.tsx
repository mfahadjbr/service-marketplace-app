"use client"

import { useState, useEffect } from "react"
import { ArrowLeft, Building2, MapPin, Clock, DollarSign } from "lucide-react"
import { useRouter } from "next/navigation"

export default function BusinessDetails() {
  const router = useRouter()
  const [formData, setFormData] = useState({
    businessName: "",
    serviceType: "",
    hourlyRate: "",
    location: "",
    workingHours: "",
  })

  useEffect(() => {
    // Check if provider is logged in
    const currentProvider = localStorage.getItem('currentProvider')
    if (!currentProvider) {
      router.push('/signup/provider/signin')
    }
  }, [router])

  const handleBack = () => {
    router.push("/signup/provider/signin")
  }

  const handleSubmit = () => {
    // Get current provider data
    const currentProvider = JSON.parse(localStorage.getItem('currentProvider') || '{}')
    
    // Add business details
    const updatedProvider = {
      ...currentProvider,
      ...formData,
      id: Date.now(), // Generate unique ID
      rating: 0,
      reviews: 0,
      isVerified: false,
      image: "/images/placeholder.jpg"
    }

    // Get existing providers
    const providers = JSON.parse(localStorage.getItem('providers') || '[]')
    
    // Add new provider
    providers.push(updatedProvider)
    
    // Save updated providers list
    localStorage.setItem('providers', JSON.stringify(providers))
    
    // Update current provider session
    localStorage.setItem('currentProvider', JSON.stringify(updatedProvider))
    
    // Redirect to dashboard
    router.push("/provider/dashboard")
  }

  const handleInputChange = (field: string, value: string) => {
    setFormData((prev) => ({ ...prev, [field]: value }))
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 px-4 py-4">
        <div className="flex items-center">
          <button onClick={handleBack} className="mr-4">
            <ArrowLeft className="w-5 h-5 text-gray-600" />
          </button>
          <div>
            <h1 className="text-lg font-semibold text-gray-900">Business Details</h1>
            <p className="text-sm text-gray-600">Step 2 of 2</p>
          </div>
        </div>
      </div>

      {/* Progress indicator */}
      <div className="bg-white px-6 py-4">
        <div className="max-w-md mx-auto">
          <div className="flex items-center">
            <div className="flex-1">
              <div className="h-2 bg-green-500 rounded-full"></div>
              <p className="text-xs text-green-600 mt-1 font-medium">Personal Info</p>
            </div>
            <div className="flex-1 ml-4">
              <div className="h-2 bg-green-500 rounded-full"></div>
              <p className="text-xs text-green-600 mt-1 font-medium">Business Details</p>
            </div>
          </div>
        </div>
      </div>

      {/* Form */}
      <div className="max-w-md mx-auto px-4 py-8">
        <div className="bg-white rounded-2xl p-6 shadow-lg">
          <div className="space-y-4">
            {/* Business Name */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Business Name</label>
              <div className="relative">
                <Building2 className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                <input
                  type="text"
                  placeholder="Your Business Name"
                  value={formData.businessName}
                  onChange={(e) => handleInputChange("businessName", e.target.value)}
                  className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-300"
                />
              </div>
            </div>

            {/* Service Type */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Service Type</label>
              <div className="relative">
                <Building2 className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                <select
                  value={formData.serviceType}
                  onChange={(e) => handleInputChange("serviceType", e.target.value)}
                  className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-300 appearance-none bg-white"
                >
                  <option value="">Select a service type</option>
                  <option value="Cleaning">Cleaning</option>
                  <option value="Plumbing">Plumbing</option>
                  <option value="Electrical">Electrical</option>
                  <option value="Painting">Painting</option>
                  <option value="Carpentry">Carpentry</option>
                  <option value="Landscaping">Landscaping</option>
                </select>
              </div>
            </div>

            {/* Hourly Rate */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Hourly Rate ($)</label>
              <div className="relative">
                <DollarSign className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                <input
                  type="number"
                  placeholder="50"
                  value={formData.hourlyRate}
                  onChange={(e) => handleInputChange("hourlyRate", e.target.value)}
                  className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-300"
                />
              </div>
            </div>

            {/* Location */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Location</label>
              <div className="relative">
                <MapPin className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                <input
                  type="text"
                  placeholder="City, State"
                  value={formData.location}
                  onChange={(e) => handleInputChange("location", e.target.value)}
                  className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-300"
                />
              </div>
            </div>

            {/* Working Hours */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Working Hours</label>
              <div className="relative">
                <Clock className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                <input
                  type="text"
                  placeholder="9:00 AM - 5:00 PM"
                  value={formData.workingHours}
                  onChange={(e) => handleInputChange("workingHours", e.target.value)}
                  className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-300"
                />
              </div>
            </div>

            {/* Submit button */}
            <button
              onClick={handleSubmit}
              className="w-full bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 text-white font-semibold py-3 px-6 rounded-xl transition-all duration-300 shadow-lg hover:shadow-xl"
            >
              Complete Registration
            </button>
          </div>
        </div>
      </div>
    </div>
  )
} 