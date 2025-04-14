"use client";

import PDFViewComponent from "@/app/components/PDFViewComponent";
import GenerateResumeComponent from "@/app/components/GenerateResumeComponent";
import History from "@/app/components/History";

export default function MainResumeViewComponent({ selectedResume, generateNew, onShowHistory }) {
    return (
        <div className="flex w-full h-full columns-2">
            <div className="flex-1 bg-white pt-8 h-full">
                {generateNew ? (
                    <GenerateResumeComponent />
                ) : selectedResume ? (
                    <PDFViewComponent resumeName={selectedResume} />
                ) : onShowHistory ? (
                    <History />
                ) : (
                    <div>
                        <h3 className="text-center mt-4 text-xl">Select a resume to view or generate a new one.</h3>
                    </div>
                )}
            </div>
        </div>
    );
}
