"use client"

import { useState, useEffect } from "react"
import { ArrowLeft, Mail, Lock, Eye, EyeOff } from "lucide-react"
import { useRouter } from "next/navigation"

export default function ProviderSignin() {
  const router = useRouter()
  const [showPassword, setShowPassword] = useState(false)
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  })
  const [isNewSignup, setIsNewSignup] = useState(false)

  useEffect(() => {
    // Check if user just signed up
    const signupData = localStorage.getItem('providerSignupData')
    if (signupData) {
      setIsNewSignup(true)
      const { email, password } = JSON.parse(signupData)
      setFormData({ email, password })
    }
  }, [])

  const handleBack = () => {
    router.push("/role-selection")
  }

  const handleSignin = () => {
    if (isNewSignup) {
      // Check credentials against providerSignupData
      const signupData = JSON.parse(localStorage.getItem('providerSignupData') || '{}')
      if (
        signupData.email === formData.email &&
        signupData.password === formData.password
      ) {
        // Store current provider session
        localStorage.setItem('currentProvider', JSON.stringify(signupData))
        localStorage.removeItem('providerSignupData') // Clean up signup data
        router.push("/signup/provider/business")
        return
      } else {
        alert("Invalid email or password")
        return
      }
    }
    // Existing provider flow
    const providers = JSON.parse(localStorage.getItem('providers') || '[]')
    const provider = providers.find(
      (p: any) => p.email === formData.email && p.password === formData.password
    )
    if (provider) {
      localStorage.setItem('currentProvider', JSON.stringify(provider))
      router.push("/provider/dashboard")
    } else {
      alert("Invalid email or password")
    }
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
            <h1 className="text-lg font-semibold text-gray-900">Provider Sign In</h1>
            <p className="text-sm text-gray-600">
              {isNewSignup ? "Complete your registration" : "Welcome back"}
            </p>
          </div>
        </div>
      </div>

      {/* Form */}
      <div className="max-w-md mx-auto px-4 py-8">
        <div className="bg-white rounded-2xl p-6 shadow-lg">
          <div className="space-y-4">
            {/* Email */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Email Address</label>
              <div className="relative">
                <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                <input
                  type="email"
                  placeholder="john@example.com"
                  value={formData.email}
                  onChange={(e) => handleInputChange("email", e.target.value)}
                  className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-300"
                />
              </div>
            </div>

            {/* Password */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Password</label>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                <input
                  type={showPassword ? "text" : "password"}
                  placeholder="Enter your password"
                  value={formData.password}
                  onChange={(e) => handleInputChange("password", e.target.value)}
                  className="w-full pl-10 pr-12 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-300"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 transform -translate-y-1/2 p-1 hover:bg-gray-100 rounded-lg transition-colors"
                >
                  {showPassword ? (
                    <EyeOff className="w-4 h-4 text-gray-400" />
                  ) : (
                    <Eye className="w-4 h-4 text-gray-400" />
                  )}
                </button>
              </div>
            </div>

            {/* Sign in button */}
            <button
              onClick={handleSignin}
              className="w-full bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 text-white font-semibold py-3 px-6 rounded-xl transition-all duration-300 shadow-lg hover:shadow-xl"
            >
              {isNewSignup ? "Continue to Business Details" : "Sign In"}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
} 