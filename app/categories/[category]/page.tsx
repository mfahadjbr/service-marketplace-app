"use client";
import { useParams, useRouter } from "next/navigation";
import { Wrench, Sparkles, Zap, Paintbrush, Leaf, Droplet, Star } from "lucide-react";

const categoryIcons = {
  "home-repair": <Wrench className="w-8 h-8 text-blue-500" />,
  cleaning: <Sparkles className="w-8 h-8 text-green-500" />,
  electrical: <Zap className="w-8 h-8 text-purple-500" />,
  painting: <Paintbrush className="w-8 h-8 text-pink-500" />,
  gardening: <Leaf className="w-8 h-8 text-orange-400" />,
  plumbing: <Droplet className="w-8 h-8 text-teal-500" />,
};

// Mock services for all categories
const mockServices: { [key: string]: Array<{
  id: number;
  name: string;
  description: string;
  price: string;
  rating: number;
  reviews: number;
  image: string;
}> } = {
  "home-repair": [
    {
      id: 1,
      name: "Door Fixing",
      description: "Expert door repair and installation services.",
      price: "$40/hr",
      rating: 4.8,
      reviews: 52,
      image: "/placeholder.svg?height=80&width=80",
    },
    {
      id: 2,
      name: "Window Repair",
      description: "Quick and reliable window repair.",
      price: "$35/hr",
      rating: 4.7,
      reviews: 34,
      image: "/placeholder.svg?height=80&width=80",
    },
    {
      id: 3,
      name: "Furniture Assembly",
      description: "Professional furniture assembly for your home.",
      price: "$30/hr",
      rating: 4.9,
      reviews: 61,
      image: "/placeholder.svg?height=80&width=80",
    },
  ],
  cleaning: [
    {
      id: 1,
      name: "Deep Cleaning",
      description: "Thorough cleaning for your entire home.",
      price: "$50/hr",
      rating: 4.9,
      reviews: 80,
      image: "/placeholder.svg?height=80&width=80",
    },
    {
      id: 2,
      name: "Carpet Cleaning",
      description: "Professional carpet and rug cleaning services.",
      price: "$45/hr",
      rating: 4.8,
      reviews: 60,
      image: "/placeholder.svg?height=80&width=80",
    },
  ],
  electrical: [
    {
      id: 1,
      name: "Light Installation",
      description: "Safe and efficient light fixture installation.",
      price: "$60/hr",
      rating: 4.7,
      reviews: 40,
      image: "/placeholder.svg?height=80&width=80",
    },
    {
      id: 2,
      name: "Wiring Repair",
      description: "Expert electrical wiring repair and troubleshooting.",
      price: "$70/hr",
      rating: 4.8,
      reviews: 35,
      image: "/placeholder.svg?height=80&width=80",
    },
  ],
  painting: [
    {
      id: 1,
      name: "Interior Painting",
      description: "High-quality interior wall and ceiling painting.",
      price: "$55/hr",
      rating: 4.9,
      reviews: 50,
      image: "/placeholder.svg?height=80&width=80",
    },
    {
      id: 2,
      name: "Exterior Painting",
      description: "Durable and beautiful exterior painting services.",
      price: "$65/hr",
      rating: 4.8,
      reviews: 42,
      image: "/placeholder.svg?height=80&width=80",
    },
  ],
  gardening: [
    {
      id: 1,
      name: "Lawn Mowing",
      description: "Keep your lawn neat and healthy.",
      price: "$25/hr",
      rating: 4.7,
      reviews: 30,
      image: "/placeholder.svg?height=80&width=80",
    },
    {
      id: 2,
      name: "Garden Design",
      description: "Custom garden design and landscaping.",
      price: "$80/hr",
      rating: 4.9,
      reviews: 22,
      image: "/placeholder.svg?height=80&width=80",
    },
  ],
  plumbing: [
    {
      id: 1,
      name: "Leak Repair",
      description: "Fast and reliable leak detection and repair.",
      price: "$50/hr",
      rating: 4.8,
      reviews: 45,
      image: "/placeholder.svg?height=80&width=80",
    },
    {
      id: 2,
      name: "Drain Cleaning",
      description: "Professional drain cleaning services.",
      price: "$40/hr",
      rating: 4.7,
      reviews: 38,
      image: "/placeholder.svg?height=80&width=80",
    },
  ],
};

export default function CategoryServicesPage() {
  const params = useParams();
  const router = useRouter();
  let categoryParam = params.category;
  let category = "";
  if (Array.isArray(categoryParam)) {
    category = categoryParam[0] || "";
  } else if (typeof categoryParam === "string") {
    category = categoryParam;
  }
  const services = mockServices[category] || [];

  return (
    <div className="min-h-screen bg-[#eaf2ff] py-12 px-2">
      <div className="max-w-4xl mx-auto">
        <div className="flex items-center gap-4 mb-8 justify-center">
          {categoryIcons[category as keyof typeof categoryIcons]}
          <h1 className="text-3xl font-bold text-gray-900 capitalize">
            {category.replace(/-/g, " ")} Services
          </h1>
        </div>
        {services.length === 0 ? (
          <div className="text-center text-gray-600">No services found for this category.</div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-8">
            {services.map((service: any) => (
              <div
                key={service.id}
                className="bg-white/80 backdrop-blur-sm rounded-2xl p-6 shadow-xl border border-gray-200 flex flex-col items-center hover:shadow-2xl hover:scale-105 transition-all duration-300"
              >
                <img
                  src={service.image}
                  alt={service.name}
                  className="w-16 h-16 rounded-xl object-cover mb-4 shadow-lg"
                />
                <h2 className="text-xl font-bold text-gray-900 mb-2 text-center">{service.name}</h2>
                <p className="text-gray-600 mb-2 text-center">{service.description}</p>
                <div className="flex items-center gap-2 mb-2">
                  <Star className="w-4 h-4 text-yellow-400 fill-current" />
                  <span className="font-semibold">{service.rating}</span>
                  <span className="text-gray-500 text-sm">({service.reviews})</span>
                </div>
                <div className="text-lg font-bold text-blue-600 mb-2">{service.price}</div>
                <div className="flex gap-2 w-full justify-center">
                  <button className="px-6 py-2 bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white font-semibold rounded-xl transition-all duration-300 shadow-lg hover:shadow-xl">
                    Book Service
                  </button>
                  <button
                    className="px-6 py-2 bg-white border border-blue-500 text-blue-600 font-semibold rounded-xl transition-all duration-300 shadow hover:bg-blue-50"
                    onClick={() => router.push(`/categories/${category}/service/${service.id}`)}
                  >
                    Details
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
} 