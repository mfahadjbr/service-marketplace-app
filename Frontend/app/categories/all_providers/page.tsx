"use client"

import { Heart, Star, MapPin } from "lucide-react"
import { useEffect, useState } from "react"

interface Provider {
  id: number
  name: string
  service: string
  rating: number
  reviews: number
  price: string
  distance: string
  image: string
  verified: boolean
  businessName: string
  serviceType: string
  hourlyRate: string
  location: string
  workingHours: string
  description: string
}

// Featured providers data (same as in categories page)
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

export default function AllProvidersPage() {
  const [providers, setProviders] = useState<Provider[]>(featuredProviders)

  useEffect(() => {
    // Fetch providers from localStorage
    const storedProviders = JSON.parse(localStorage.getItem('providers') || '[]')
    
    // Transform the data to match the required format
    const formattedProviders = storedProviders.map((provider: any) => ({
      id: provider.id,
      name: `${provider.firstName} ${provider.lastName}`,
      service: provider.serviceType,
      rating: provider.rating || 0,
      reviews: provider.reviews || 0,
      price: `$${provider.hourlyRate}/hr`,
      distance: provider.distance || "0 km",
      image: provider.image || "/placeholder.svg?height=80&width=80",
      verified: provider.verified || false,
      businessName: provider.businessName,
      serviceType: provider.serviceType,
      hourlyRate: provider.hourlyRate,
      location: provider.location,
      workingHours: provider.workingHours,
      description: provider.description
    }))
    
    // Combine featured providers with actual providers
    // Filter out any duplicates based on business name
    const uniqueProviders = formattedProviders.filter(
      (provider: Provider) => !featuredProviders.some((fp) => fp.businessName === provider.businessName)
    )
    
    setProviders([...featuredProviders, ...uniqueProviders])
  }, [])

  return (
    <div className="min-h-screen bg-[#eaf2ff] py-12 px-2">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-8 text-center">All Providers</h1>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {providers.map((provider) => (
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
