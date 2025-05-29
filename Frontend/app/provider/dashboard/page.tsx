"use client"

import { Search, Bell, User, Star, MapPin, Calendar, DollarSign, Clock, LogOut } from "lucide-react"
import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"

interface Provider {
  id: number
  firstName: string
  lastName: string
  email: string
  phone: string
  businessName: string
  serviceType: string
  hourlyRate: string
  location: string
  workingHours: string
  description: string
  rating: number
  reviews: number
}

interface Booking {
  id: number
  providerId: number
  customerName: string
  service: string
  date: string
  duration: string
  price: string
  status: string
}

interface Review {
  id: number
  providerId: number
  customerName: string
  rating: number
  comment: string
  date: string
}

export default function ProviderDashboard() {
  const router = useRouter()
  const [provider, setProvider] = useState<Provider | null>(null)
  const [bookings, setBookings] = useState<Booking[]>([])
  const [reviews, setReviews] = useState<Review[]>([])
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    // Check if provider is logged in
    const currentProvider = JSON.parse(localStorage.getItem('currentProvider') || 'null')
    if (!currentProvider) {
      router.push('/signup/provider/signin')
      return
    }

    // Get provider's bookings from localStorage
    const allBookings = JSON.parse(localStorage.getItem('bookings') || '[]')
    const providerBookings = allBookings.filter((booking: Booking) => booking.providerId === currentProvider.id)
    
    // Get provider's reviews from localStorage
    const allReviews = JSON.parse(localStorage.getItem('reviews') || '[]')
    const providerReviews = allReviews.filter((review: Review) => review.providerId === currentProvider.id)

    setProvider(currentProvider)
    setBookings(providerBookings)
    setReviews(providerReviews)
    setIsLoading(false)
  }, [router])

  const handleLogout = () => {
    localStorage.removeItem('currentProvider')
    router.push('/')
  }

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-green-50 to-emerald-100 flex items-center justify-center">
        <div className="text-2xl font-semibold text-gray-700">Loading...</div>
      </div>
    )
  }

  if (!provider) {
    return null
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-green-50 to-emerald-100">
      {/* Header */}
      <div className="bg-white/80 backdrop-blur-sm border-b border-gray-200 sticky top-0 z-10">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-xl lg:text-2xl font-bold text-gray-900">
                Welcome back, {provider.firstName}! 👋
              </h1>
              <p className="text-gray-600">{provider.businessName} - {provider.serviceType}</p>
            </div>
            <div className="flex items-center space-x-3">
              <button className="p-3 bg-gradient-to-br from-gray-100 to-gray-200 rounded-xl hover:from-gray-200 hover:to-gray-300 transition-all duration-300 shadow-lg">
                <Bell className="w-5 h-5 text-gray-600" />
              </button>
              <button 
                onClick={handleLogout}
                className="p-3 bg-gradient-to-br from-red-400 to-red-600 rounded-xl hover:from-red-500 hover:to-red-700 transition-all duration-300 shadow-lg"
              >
                <LogOut className="w-5 h-5 text-white" />
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-8">
        {/* Provider Info Card */}
        <div className="bg-white/80 backdrop-blur-sm p-6 rounded-2xl border border-gray-200 shadow-lg mb-8">
          <div className="flex items-start justify-between">
            <div>
              <h2 className="text-xl font-bold text-gray-900 mb-2">Business Information</h2>
              <div className="space-y-2">
                <p className="text-gray-600">
                  <span className="font-semibold">Business Name:</span> {provider.businessName}
                </p>
                <p className="text-gray-600">
                  <span className="font-semibold">Service Type:</span> {provider.serviceType}
                </p>
                <p className="text-gray-600">
                  <span className="font-semibold">Hourly Rate:</span> ${provider.hourlyRate}/hr
                </p>
                <p className="text-gray-600">
                  <span className="font-semibold">Location:</span> {provider.location}
                </p>
                <p className="text-gray-600">
                  <span className="font-semibold">Working Hours:</span> {provider.workingHours}
                </p>
                <p className="text-gray-600">
                  <span className="font-semibold">Email:</span> {provider.email}
                </p>
                <p className="text-gray-600">
                  <span className="font-semibold">Phone:</span> {provider.phone}
                </p>
              </div>
            </div>
            <button className="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors">
              Edit Profile
            </button>
          </div>
        </div>

        {/* Stats Overview */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white/80 backdrop-blur-sm p-6 rounded-2xl border border-gray-200 shadow-lg">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600">Today's Earnings</p>
                <h3 className="text-2xl font-bold text-gray-900">
                  ${bookings
                    .filter(booking => booking.status === "confirmed")
                    .reduce((total, booking) => total + parseInt(booking.price.replace('$', '')), 0)}
                </h3>
              </div>
              <div className="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center">
                <DollarSign className="w-6 h-6 text-green-600" />
              </div>
            </div>
          </div>
          <div className="bg-white/80 backdrop-blur-sm p-6 rounded-2xl border border-gray-200 shadow-lg">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600">Upcoming Bookings</p>
                <h3 className="text-2xl font-bold text-gray-900">{bookings.length}</h3>
              </div>
              <div className="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center">
                <Calendar className="w-6 h-6 text-blue-600" />
              </div>
            </div>
          </div>
          <div className="bg-white/80 backdrop-blur-sm p-6 rounded-2xl border border-gray-200 shadow-lg">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600">Average Rating</p>
                <h3 className="text-2xl font-bold text-gray-900">
                  {reviews.length > 0
                    ? (reviews.reduce((acc, review) => acc + review.rating, 0) / reviews.length).toFixed(1)
                    : "0.0"}
                </h3>
              </div>
              <div className="w-12 h-12 bg-yellow-100 rounded-xl flex items-center justify-center">
                <Star className="w-6 h-6 text-yellow-600" />
              </div>
            </div>
          </div>
        </div>

        {/* Upcoming Bookings */}
        <div className="mb-8">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold text-gray-900">Upcoming Bookings</h2>
            <button className="text-green-600 hover:text-green-700 font-semibold">View all</button>
          </div>
          <div className="space-y-4">
            {bookings.length > 0 ? (
              bookings.map((booking) => (
                <div
                  key={booking.id}
                  className="bg-white/80 backdrop-blur-sm p-6 rounded-2xl border border-gray-200 hover:shadow-xl transition-all duration-300"
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-4">
                      <div className="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center">
                        <User className="w-6 h-6 text-green-600" />
                      </div>
                      <div>
                        <h3 className="font-semibold text-gray-900">{booking.customerName}</h3>
                        <p className="text-gray-600">{booking.service}</p>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="font-semibold text-gray-900">{booking.price}</p>
                      <p className="text-sm text-gray-500">{booking.duration}</p>
                    </div>
                  </div>
                  <div className="mt-4 flex items-center justify-between">
                    <div className="flex items-center space-x-4">
                      <div className="flex items-center space-x-1">
                        <Clock className="w-4 h-4 text-gray-400" />
                        <span className="text-sm text-gray-600">{booking.date}</span>
                      </div>
                    </div>
                    <span
                      className={`px-3 py-1 rounded-full text-sm font-medium ${
                        booking.status === "confirmed"
                          ? "bg-green-100 text-green-700"
                          : "bg-yellow-100 text-yellow-700"
                      }`}
                    >
                      {booking.status}
                    </span>
                  </div>
                </div>
              ))
            ) : (
              <div className="text-center py-8 text-gray-500">
                No upcoming bookings
              </div>
            )}
          </div>
        </div>

        {/* Recent Reviews */}
        <div>
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold text-gray-900">Recent Reviews</h2>
            <button className="text-green-600 hover:text-green-700 font-semibold">View all</button>
          </div>
          <div className="space-y-4">
            {reviews.length > 0 ? (
              reviews.map((review) => (
                <div
                  key={review.id}
                  className="bg-white/80 backdrop-blur-sm p-6 rounded-2xl border border-gray-200 hover:shadow-xl transition-all duration-300"
                >
                  <div className="flex items-start justify-between">
                    <div className="flex items-center space-x-4">
                      <div className="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center">
                        <User className="w-6 h-6 text-green-600" />
                      </div>
                      <div>
                        <h3 className="font-semibold text-gray-900">{review.customerName}</h3>
                        <div className="flex items-center space-x-1">
                          {[...Array(5)].map((_, i) => (
                            <Star
                              key={i}
                              className={`w-4 h-4 ${
                                i < review.rating ? "text-yellow-400 fill-current" : "text-gray-300"
                              }`}
                            />
                          ))}
                        </div>
                      </div>
                    </div>
                    <span className="text-sm text-gray-500">{review.date}</span>
                  </div>
                  <p className="mt-4 text-gray-600">{review.comment}</p>
                </div>
              ))
            ) : (
              <div className="text-center py-8 text-gray-500">
                No reviews yet
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
} 