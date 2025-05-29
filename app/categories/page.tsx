"use client"

import { Wrench, Sparkles, Zap, Paintbrush, Leaf, Droplet, LogOut, Heart, Star, MapPin } from "lucide-react"
import { useRouter, useParams } from "next/navigation"
import Link from "next/link"

const categories = [
  {
    name: "Home Repair",
    slug: "home-repair",
    icon: <Wrench className="w-8 h-8" />, 
    bg: "bg-blue-100",
    iconBg: "bg-blue-500",
  },
  {
    name: "Cleaning",
    slug: "cleaning",
    icon: <Sparkles className="w-8 h-8" />, 
    bg: "bg-green-100",
    iconBg: "bg-green-500",
  },
  {
    name: "Electrical",
    slug: "electrical",
    icon: <Zap className="w-8 h-8" />, 
    bg: "bg-purple-100",
    iconBg: "bg-purple-500",
  },
  {
    name: "Painting",
    slug: "painting",
    icon: <Paintbrush className="w-8 h-8" />, 
    bg: "bg-pink-100",
    iconBg: "bg-pink-500",
  },
  {
    name: "Gardening",
    slug: "gardening",
    icon: <Leaf className="w-8 h-8" />, 
    bg: "bg-yellow-100",
    iconBg: "bg-orange-400",
  },
  {
    name: "Plumbing",
    slug: "plumbing",
    icon: <Droplet className="w-8 h-8" />, 
    bg: "bg-teal-100",
    iconBg: "bg-teal-500",
  },
]

const featuredProviders = [
  {
    id: 1,
    name: "Sarah Johnson",
    service: "House Cleaning",
    rating: 4.9,
    reviews: 127,
    price: "$25/hr",
    distance: "2.3 km",
    image: "/placeholder.svg?height=80&width=80",
    verified: true,
    businessName: "Sparkle & Shine Cleaning",
    serviceType: "House Cleaning",
    hourlyRate: "25",
    location: "Downtown",
    workingHours: "Mon-Fri 9AM-5PM",
    description: "Professional cleaning services"
  },
  {
    id: 2,
    name: "Mike Chen",
    service: "Plumbing",
    rating: 4.8,
    reviews: 89,
    price: "$45/hr",
    distance: "1.8 km",
    image: "/placeholder.svg?height=80&width=80",
    verified: true,
    businessName: "Quick Fix Plumbing",
    serviceType: "Plumbing",
    hourlyRate: "45",
    location: "Westside",
    workingHours: "24/7 Emergency Service",
    description: "Expert plumbing solutions"
  },
  {
    id: 3,
    name: "Emma Davis",
    service: "Electrical Work",
    rating: 4.9,
    reviews: 156,
    price: "$55/hr",
    distance: "3.1 km",
    image: "/placeholder.svg?height=80&width=80",
    verified: true,
    businessName: "Safe & Sound Electrical",
    serviceType: "Electrical",
    hourlyRate: "55",
    location: "Eastside",
    workingHours: "Mon-Sat 8AM-6PM",
    description: "Licensed electrical services"
  }
]

export default function CategoriesPage() {
  const router = useRouter()
  const params = useParams()
  const category = params.category

  const handleLogout = () => {
    // Clear any auth/session here
    router.push("/")
  }

  return (
    <div className="min-h-screen bg-[#eaf2ff]">
      {/* Header */}
      <div className="flex items-center justify-between px-8 py-6 bg-white/80 backdrop-blur-sm border-b border-gray-200 sticky top-0 z-10">
        <h1 className="text-2xl font-bold text-gray-900">SYS AI PLATFORM</h1>
        <div className="flex items-center gap-6">
          <button
            onClick={handleLogout}
            className="flex items-center gap-2 px-4 py-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <LogOut className="w-5 h-5" />
            <span>Logout</span>
          </button>
        </div>
      </div>

      {/* Service Categories Header */}
      <div className="flex items-center justify-between max-w-5xl mx-auto px-4 pt-12 pb-4">
        <h1 className="text-2xl font-bold text-gray-900">Service Categories</h1>
        <button
          className="text-blue-600 hover:text-blue-700 font-semibold text-lg transition-colors"
          onClick={() => router.push('/categories/all_categories')}
        >
          See all
        </button>
      </div>

      {/* Categories Grid */}
      <div className="max-w-5xl mx-auto px-4 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-8">
        {categories.map((cat) => (
          <div
            key={cat.name}
            onClick={() => router.push(`/categories/${cat.slug}`)}
            className={`rounded-2xl shadow-md flex flex-col items-center justify-center p-8 ${cat.bg} transition-transform duration-200 hover:scale-105 hover:shadow-xl cursor-pointer`}
          >
            <div className={`mb-4 rounded-xl p-4 shadow ${cat.iconBg} text-white flex items-center justify-center`}>
              {cat.icon}
            </div>
            <div className="text-lg font-semibold text-gray-800 text-center">{cat.name}</div>
          </div>
        ))}
      </div>

      {/* Featured Providers */}
      <div className="max-w-6xl mx-auto px-4 py-7">
        <div className="flex justify-between items-center mb-8">
          <h2 className="text-2xl lg:text-3xl font-bold text-gray-900">Featured Providers</h2>
          <Link
            href="/categories/all_providers"
            className="text-blue-600 hover:text-blue-700 font-semibold text-lg transition-colors"
          >
            View all
          </Link>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {featuredProviders.map((provider) => (
            <div
              key={provider.id}
              className="group bg-white/80 backdrop-blur-sm p-6 rounded-2xl border border-gray-200 hover:shadow-xl transition-all duration-300 hover:scale-105"
            >
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center space-x-4">
                  <div className="relative">
                    <img
                      src={provider.image}
                      alt={provider.name}
                      className="w-16 h-16 rounded-2xl object-cover shadow-lg"
                    />
                    {provider.verified && (
                      <div className="absolute -top-1 -right-1 w-6 h-6 bg-gradient-to-br from-green-400 to-green-600 rounded-full flex items-center justify-center">
                        <div className="w-3 h-3 bg-white rounded-full"></div>
                      </div>
                    )}
                  </div>
                  <div>
                    <h3 className="font-bold text-gray-900 text-lg">{provider.businessName}</h3>
                    <p className="text-gray-600">{provider.serviceType}</p>
                  </div>
                </div>
                <button className="p-2 hover:bg-gray-100 rounded-xl transition-colors">
                  <Heart className="w-5 h-5 text-gray-400 hover:text-red-500" />
                </button>
              </div>

              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center space-x-4">
                  <div className="flex items-center space-x-1">
                    <Star className="w-4 h-4 text-yellow-400 fill-current" />
                    <span className="font-semibold">{provider.rating}</span>
                    <span className="text-gray-500 text-sm">({provider.reviews})</span>
                  </div>
                  <div className="flex items-center space-x-1">
                    <MapPin className="w-4 h-4 text-gray-400" />
                    <span className="text-gray-500 text-sm">{provider.location}</span>
                  </div>
                </div>
              </div>

              <div className="flex items-center justify-between">
                <div>
                  <p className="text-2xl font-bold text-gray-900">{provider.price}</p>
                  <p className="text-gray-500 text-sm">Starting price</p>
                </div>
                <button className="px-6 py-3 bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 text-white font-semibold rounded-xl transition-all duration-300 shadow-lg hover:shadow-xl">
                  Book Now
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
} 