/**
 * Crisis screen component
 * Displays crisis resources and locks session
 */

"use client";

import { CrisisResource } from "@/lib/types";

interface CrisisScreenProps {
  message: string;
  resources: CrisisResource[];
}

export function CrisisScreen({ message, resources }: CrisisScreenProps) {
  return (
    <div className="flex-1 overflow-y-auto px-4 py-8">
      <div className="max-w-2xl mx-auto">
        <div className="bg-red-50 border border-red-200 rounded-lg p-6 mb-6">
          <h2 className="text-xl font-semibold text-red-900 mb-4">
            Crisis Support
          </h2>
          <p className="whitespace-pre-wrap text-red-900 leading-relaxed">
            {message}
          </p>
        </div>

        <div className="space-y-4">
          {resources.map((resource, index) => (
            <div
              key={index}
              className="bg-white border border-gray-200 rounded-lg p-6"
            >
              <h3 className="font-semibold text-gray-900 mb-2">
                {resource.name}
              </h3>
              <p className="text-2xl font-bold text-gray-900 mb-2">
                {resource.phone}
              </p>
              <p className="text-sm text-gray-600 mb-1">
                Available: {resource.available}
              </p>
              {resource.description && (
                <p className="text-sm text-gray-700 mt-2">
                  {resource.description}
                </p>
              )}
            </div>
          ))}
        </div>

        <div className="mt-8 p-4 bg-gray-50 rounded-lg">
          <p className="text-sm text-gray-700 text-center">
            This session is now locked. Please close this window and reach out
            to one of the resources above.
          </p>
        </div>
      </div>
    </div>
  );
}
