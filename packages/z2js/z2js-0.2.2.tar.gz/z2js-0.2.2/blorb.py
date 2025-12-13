"""
Blorb file parser for Z-Machine multimedia resources

Blorb is an IFF-based container format that packages:
- Z-machine story file (ZCOD chunk)
- Pictures (PNG, JPEG, or Rect placeholders)
- Sounds (AIFF, MOD, or Ogg)
- Metadata and resource index

IFF structure:
- FORM chunk containing all data
- RIdx (Resource Index) - maps resource numbers to chunk offsets
- Chunks for each resource type
"""

import struct
from typing import Dict, List, Tuple, Optional, BinaryIO
from dataclasses import dataclass
from enum import Enum


class ResourceType(Enum):
    """Types of resources in a Blorb file"""
    PICTURE = b'Pict'
    SOUND = b'Snd '
    EXECUTABLE = b'Exec'
    DATA = b'Data'


@dataclass
class Resource:
    """Represents a resource in the Blorb file"""
    type: ResourceType
    number: int
    offset: int
    length: int
    chunk_type: bytes  # e.g., b'PNG ', b'JPEG', b'AIFF', b'OGGV', b'ZCOD'
    data: Optional[bytes] = None


@dataclass
class BlorbMetadata:
    """Metadata from the Blorb file"""
    ifid: Optional[str] = None  # IFID from IFmd chunk
    title: Optional[str] = None
    author: Optional[str] = None
    description: Optional[str] = None
    release_date: Optional[str] = None
    # Frontispiece (cover image) resource number
    frontispiece: Optional[int] = None


class BlorbParser:
    """Parser for Blorb (.blorb, .zblorb, .gblorb) files"""

    def __init__(self, data: bytes):
        self.data = data
        self.resources: Dict[Tuple[ResourceType, int], Resource] = {}
        self.pictures: Dict[int, Resource] = {}
        self.sounds: Dict[int, Resource] = {}
        self.executable: Optional[bytes] = None
        self.metadata = BlorbMetadata()
        self._parse()

    def _read_chunk_header(self, offset: int) -> Tuple[bytes, int]:
        """Read a chunk header (4-byte type, 4-byte length)"""
        chunk_type = self.data[offset:offset+4]
        chunk_length = struct.unpack('>I', self.data[offset+4:offset+8])[0]
        return chunk_type, chunk_length

    def _parse(self) -> None:
        """Parse the Blorb file structure"""
        # Check for FORM header
        if self.data[:4] != b'FORM':
            raise ValueError("Not a valid IFF/Blorb file: missing FORM header")

        form_length = struct.unpack('>I', self.data[4:8])[0]
        form_type = self.data[8:12]

        if form_type != b'IFRS':
            raise ValueError(f"Not a Blorb file: expected IFRS, got {form_type}")

        # Parse chunks
        offset = 12  # Start after FORM header
        end = 8 + form_length

        while offset < end:
            chunk_type, chunk_length = self._read_chunk_header(offset)
            chunk_data_start = offset + 8
            chunk_data = self.data[chunk_data_start:chunk_data_start + chunk_length]

            self._process_chunk(chunk_type, chunk_data, chunk_data_start)

            # Move to next chunk (chunks are padded to even length)
            offset += 8 + chunk_length
            if chunk_length % 2 == 1:
                offset += 1

    def _process_chunk(self, chunk_type: bytes, data: bytes, data_offset: int) -> None:
        """Process a single chunk"""
        if chunk_type == b'RIdx':
            self._parse_resource_index(data)
        elif chunk_type == b'IFmd':
            self._parse_metadata(data)
        elif chunk_type == b'Fspc':
            # Frontispiece - cover image resource number
            if len(data) >= 4:
                self.metadata.frontispiece = struct.unpack('>I', data[:4])[0]
        elif chunk_type == b'AUTH':
            self.metadata.author = data.rstrip(b'\x00').decode('latin-1')
        elif chunk_type == b'(c) ':
            # Copyright notice
            pass
        elif chunk_type == b'ANNO':
            # Annotation
            pass
        elif chunk_type in (b'PNG ', b'JPEG', b'Rect'):
            # Picture data - will be loaded via resource index
            pass
        elif chunk_type in (b'AIFF', b'OGGV', b'MOD '):
            # Sound data - will be loaded via resource index
            pass
        elif chunk_type == b'ZCOD':
            # Z-code executable
            self.executable = data
        elif chunk_type == b'GLUL':
            # Glulx executable
            self.executable = data

    def _parse_resource_index(self, data: bytes) -> None:
        """Parse the RIdx (Resource Index) chunk"""
        num_resources = struct.unpack('>I', data[:4])[0]
        offset = 4

        for _ in range(num_resources):
            usage = data[offset:offset+4]
            number = struct.unpack('>I', data[offset+4:offset+8])[0]
            start = struct.unpack('>I', data[offset+8:offset+12])[0]
            offset += 12

            # Read the chunk at the specified offset
            chunk_type, chunk_length = self._read_chunk_header(start)

            # Determine resource type from usage
            if usage == b'Pict':
                res_type = ResourceType.PICTURE
            elif usage == b'Snd ':
                res_type = ResourceType.SOUND
            elif usage == b'Exec':
                res_type = ResourceType.EXECUTABLE
            elif usage == b'Data':
                res_type = ResourceType.DATA
            else:
                continue

            resource = Resource(
                type=res_type,
                number=number,
                offset=start + 8,  # Skip chunk header
                length=chunk_length,
                chunk_type=chunk_type
            )

            self.resources[(res_type, number)] = resource

            if res_type == ResourceType.PICTURE:
                self.pictures[number] = resource
            elif res_type == ResourceType.SOUND:
                self.sounds[number] = resource
            elif res_type == ResourceType.EXECUTABLE:
                self.executable = self.data[resource.offset:resource.offset + resource.length]

    def _parse_metadata(self, data: bytes) -> None:
        """Parse the IFmd metadata chunk (Treaty of Babel format)"""
        try:
            xml_str = data.decode('utf-8')
            # Simple XML parsing for key fields
            import re

            ifid_match = re.search(r'<ifid>([^<]+)</ifid>', xml_str)
            if ifid_match:
                self.metadata.ifid = ifid_match.group(1)

            title_match = re.search(r'<title>([^<]+)</title>', xml_str)
            if title_match:
                self.metadata.title = title_match.group(1)

            author_match = re.search(r'<author>([^<]+)</author>', xml_str)
            if author_match:
                self.metadata.author = author_match.group(1)

            desc_match = re.search(r'<description>([^<]+)</description>', xml_str)
            if desc_match:
                self.metadata.description = desc_match.group(1)

        except Exception:
            pass  # Ignore metadata parsing errors

    def get_resource_data(self, res_type: ResourceType, number: int) -> Optional[bytes]:
        """Get the raw data for a resource"""
        key = (res_type, number)
        if key not in self.resources:
            return None

        resource = self.resources[key]
        if resource.data is None:
            resource.data = self.data[resource.offset:resource.offset + resource.length]

        return resource.data

    def get_picture(self, number: int) -> Optional[Tuple[bytes, str]]:
        """Get picture data and format (png, jpeg, or rect)"""
        if number not in self.pictures:
            return None

        resource = self.pictures[number]
        data = self.get_resource_data(ResourceType.PICTURE, number)

        if resource.chunk_type == b'PNG ':
            return (data, 'png')
        elif resource.chunk_type == b'JPEG':
            return (data, 'jpeg')
        elif resource.chunk_type == b'Rect':
            # Placeholder rectangle - 4 bytes width, 4 bytes height
            return (data, 'rect')

        return None

    def get_sound(self, number: int) -> Optional[Tuple[bytes, str]]:
        """Get sound data and format (aiff, ogg, or mod)"""
        if number not in self.sounds:
            return None

        resource = self.sounds[number]
        data = self.get_resource_data(ResourceType.SOUND, number)

        if resource.chunk_type == b'AIFF':
            return (data, 'aiff')
        elif resource.chunk_type == b'OGGV':
            return (data, 'ogg')
        elif resource.chunk_type == b'MOD ':
            return (data, 'mod')

        return None

    def get_story_file(self) -> Optional[bytes]:
        """Get the embedded story file (Z-code or Glulx)"""
        return self.executable

    def list_pictures(self) -> List[int]:
        """List all picture resource numbers"""
        return sorted(self.pictures.keys())

    def list_sounds(self) -> List[int]:
        """List all sound resource numbers"""
        return sorted(self.sounds.keys())


def is_blorb_file(data: bytes) -> bool:
    """Check if data is a Blorb file"""
    return len(data) >= 12 and data[:4] == b'FORM' and data[8:12] == b'IFRS'


def extract_story_from_blorb(data: bytes) -> Optional[bytes]:
    """Extract the story file from a Blorb container"""
    if not is_blorb_file(data):
        return None

    try:
        parser = BlorbParser(data)
        return parser.get_story_file()
    except Exception:
        return None
