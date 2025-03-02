import Link from "next/link";
import HeroComponent from "@/app/components/HeroComponent";
import NavComponent from "@/app/components/NavComponent";

export default async function Home() {
    return (
        <div className="w-full min-h-screen pb-20 gap-8 font-[family-name:var(--font-geist-sans)]
         flex flex-col items-center">
            <NavComponent></NavComponent>
            <main className="main-layout">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-10 w-full">
                    <div className="flex flex-col items-center justify-center text-left">
                        <div>
                            <h1 className="text-7xl pb-5 text-left">
                                <hr className="button-blue text-blue-500 w-1/3 pb-1.5 mb-6" />
                                A tailored resumé, <br/> any internship, <br/> in seconds.
                            </h1>
                            <h2 className="text-2xl pb-5">Wondering how it works?</h2>
                            <button
                                className="button-blue
                            text-white font-bold text-2xl py-2 px-10 rounded">
                                GET STARTED
                            </button>
                        </div>
                    </div>
                    <div>
                        <HeroComponent/>
                    </div>
                </div>
            </main>
            <footer className="flex gap-6 flex-wrap items-center justify-center">
                {/* Footer content */}
            </footer>
        </div>
    );
}
