// swift-tools-version: 5.9
import PackageDescription

let package = Package(
    name: "MeetingMind",
    platforms: [
        .macOS(.v13)
    ],
    products: [
        .executable(
            name: "MeetingMind",
            targets: ["MeetingMind"]
        )
    ],
    dependencies: [
        .package(url: "https://github.com/groue/GRDB.swift", from: "6.0.0"),
        .package(url: "https://github.com/apple/swift-log", from: "1.5.0")
    ],
    targets: [
        .executableTarget(
            name: "MeetingMind",
            dependencies: [
                .product(name: "GRDB", package: "GRDB.swift"),
                .product(name: "Logging", package: "swift-log")
            ],
            path: "MeetingMind"
        )
    ]
)
